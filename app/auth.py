from datetime import timedelta, datetime
from typing import Annotated
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
from app.database import get_db_connection
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import DictCursor

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=[ 'bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    create_user_request: CreateUserRequest,
    db: PgConnection = Depends(get_db_connection)
    ):
    hashed_password = bcrypt_context.hash(create_user_request.password)
    try:
        with db.cursor() as cursor:
            cursor.execute(
            """
            INSERT INTO users (username, hashed_password, role)
            VALUES (%s, %s, %s)
            """,
            (create_user_request.username, hashed_password, 'visor') # Asignas un rol por defecto
            )
        db.commit()
        return{"message": "Usuario creado exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo crear el usuario: {e}"
        )
    finally:
        if db:
            db.close()

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: PgConnection = Depends(get_db_connection)
    ):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar usuario"
        )
    
    token = create_access_token(
        username=user["username"],
        user_id=user["id"],
        role=user["role"],
        expires_delta=timedelta(minutes=30)
    )
    

    return {"access_token": token, "token_type": "bearer"}

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role') 
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="No se pudo validar usuario")
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='No se pudo validar usuario')

def authenticate_user(username: str, password: str, db: PgConnection):
    try:
        with db.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            user_data = cursor.fetchone()
            if not user_data:
                return False
            if not bcrypt_context.verify(password, user_data["hashed_password"]):
                return False
            return user_data
    except Exception as e:
        print(f"Error en la base de datos durante la autenticación: {e}")
        return False
    finally:
        if db:
            db.close()