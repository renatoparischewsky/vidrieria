from sqlmodel import Session, select
from db.init_db import engine, init_db
from app.employees import Employee

# Inicializar la base de datos
init_db()

# Insertar empleado
with Session(engine) as session:
    nuevo = Employee(
        tax_id="12345678-9",
        first_name="Renato",
        last_name="Parischewsky",
        base_salary=650000
    )
    session.add(nuevo)
    session.commit()

# Consultar todos los empleados
with Session(engine) as session:
    empleados = session.exec(select(Employee)).all()
    for e in empleados:
        print(f"{e.identifier} - {e.first_name} {e.last_name} - ${e.base_salary}")
