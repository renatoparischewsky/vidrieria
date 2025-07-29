from sqlmodel import create_engine, SQLModel
from app.models import Employee

engine = create_engine("sqlite:///vidrieria.db", echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)