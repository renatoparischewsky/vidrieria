from fastapi import FastAPI, HTTPException, Query
import psycopg2
from psycopg2.extras import DictCursor
import os
from typing import List
from dotenv import load_dotenv
from employees import Employee
from movements import Movement
from calculations_movement import *
from schemas import *


load_dotenv()

app =FastAPI(title="Vidrieria API", version="1.0.0")

# Employee functions
#---------------------

def get_db_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

@app.get("/employees/load", response_model=EmployeeGet)
def load_employee_api(employee_id):
    
    loaded = Employee.load_employee(employee_id)
    if not loaded:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return loaded


@app.post("/employees/insert", status_code=200)
def insert_employee_api(employee_data: EmployeeCreate):
    employee = Employee(**employee_data.model_dump())
    success = employee.insert_employee()
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo insertar empleado")

@app.get("/employees/active", response_model=List[EmployeeGet])
def get_all_active_api():
    employees = Employee.get_all_active()
    if not employees:
        raise HTTPException(status_code=404, detail="No hay empleados activos")
    return employees

@app.get("/employees/inactive", response_model=List[EmployeeGet])
def get_all_inactive_api():
    employees = Employee.get_all_inactive()
    if not employees:
        raise HTTPException(status_code=404, detail="No hay empleados inactivos")
    return employees

    
@app.get("/employees/all", response_model=List[EmployeeGet])
def get_all_api():
    employees = Employee.get_all_employees()
    if not employees:
        raise HTTPException(status_code=404, detail="No hay empleados")
    return employees

@app.put("/employees/{employee_id}/activate", status_code=204)
def mark_as_active_api(employee_id: int):
    employee = Employee.load_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    employee.mark_as_active()



@app.put("/employees/{employee_id}/inactivate")
def mark_as_inactive_api(employee_id: int):
    employee = Employee.load_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    employee.mark_as_inactive()

@app.put("/employees/{employee_id}/update", status_code=204)
def update_employee_api(employee_id: int, employee_data: EmployeeUpdate):
    employee_to_update = Employee.load_employee(employee_id)
    if not employee_to_update:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    update_data = employee_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee_to_update, key, value)

    if not employee_to_update.update_employee():
        raise HTTPException(status_code=500, detail="No se pudo actualizar el empleado")


# Movement functions
#---------------------

@app.post("/movements/insert", status_code=200)
def insert_movement_api(movement_data: MovementCreate):
    movement = Movement(**movement_data.model_dump())
    success = movement.insert_movement()
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo insertar movimiento")

@app.get("/movements/monthly/{year}/{month}/", response_model=List[MovementGet])
def find_by_month_api(year: int, month: int):
    movements = Movement.find_by_month(year, month)
    if not movements:
        raise HTTPException(status_code=404, detail="Movimientos no encontrados")
    return movements

@app.get("/movements/date-range/", response_model=List[MovementGet])
def find_by_date_range_api(
    start_date: datetime = Query(..., description="Fecha inicio en formato ISO"),
    end_date: datetime = Query(..., description="Fecha fin en formato ISO")
):
    movements = Movement.find_by_date_range(start_date, end_date)
    if not movements:
        raise HTTPException(status_code=404, detail="Movimientos no encontrados")
    return movements

@app.get("/movements/employee/{employee_id}/monthly/{year}/{month}/", response_model=List[MovementGet])
def find_by_employee_and_month_api(employee_id: int, year: int, month: int):
    movements = Movement.find_by_employee_and_month(employee_id, year, month)
    if not movements:
        raise HTTPException(status_code=404, detail="Movimientos no encontrados")
    return movements

@app.get("/movements/employee/{employee_id}/date-range/", response_model=List[MovementGet])
def find_by_employee_and_date_range_api(
    employee_id: int,
    start_date: datetime = Query(..., description="Fecha inicio en formato ISO"),
    end_date: datetime = Query(..., description="Fecha fin en formato ISO")
):
    movements = Movement.find_by_employee_and_date_range(employee_id, start_date, end_date)
    if not movements:
        raise HTTPException(status_code=404, detail="Movimientos no encontrados")
    return movements

@app.delete("/movements/{movement_id}", status_code=200)
def delete_by_id_api(movement_id: int):
    success =Movement.delete_by_id(movement_id)
    if not success:
        raise HTTPException(status_code=404, detail="No se pudo eliminar movimiento")

# calculations_movement functions
#---------------------

@app.post("/movements/cash-advance", status_code=200)
def register_cash_advance_api(movement_data: MovementWithAmountRequest):
    result = register_cash_advance(
        employee_id=movement_data.employee_id,
        amount=movement_data.amount, 
        description=movement_data.description,
        movement_date=movement_data.movement_date.isoformat() if movement_data.movement_date else None
    )
    
    if not result:
        raise HTTPException(status_code=400, detail="No se pudo registrar adelanto")

@app.post("/movements/bank-transfer", status_code=200)
def register_bank_transfer_api(movement_data: MovementWithAmountRequest):
    result = register_bank_transfer(
        employee_id=movement_data.employee_id,
        amount=movement_data.amount, 
        description=movement_data.description,
        movement_date=movement_data.movement_date.isoformat() if movement_data.movement_date else None
    )
    
    if not result:
        raise HTTPException(status_code=400, detail="No se pudo registrar adelanto")

@app.post("/movements/absence", status_code=200)
def register_abscence_api(movement_data: BaseMovementRequest):
    result = register_abscence(
        employee_id=movement_data.employee_id,
        description=movement_data.description,
        movement_date=movement_data.movement_date.isoformat() if movement_data.movement_date else None
    )
    
    if not result:
        raise HTTPException(status_code=400, detail="No se pudo registrar adelanto")

@app.get("/payment-date/{year}/{month}")
def get_payment_date_api(year: int, month: int):
    payment_date = get_payment_date(year, month)
    if not payment_date:
        raise HTTPException(status_code=500, detail="Error calculando fecha de pago de sueldos.")
    return {
    "year": year,                                    # 2024
    "month": month,                                  # 12
    "payment_date": payment_date.isoformat(),        # "2024-12-30"
    "day_of_week": payment_date.strftime("%A"),      # "Monday"
    }

@app.get("/payroll-period/", response_model=PayrollPeriodResponse)
def get_payroll_period_api(year: int, month: int):
    start_date, end_date = get_payroll_period(year, month)
    if not start_date or not end_date:
        raise HTTPException(status_code=500, detail="Error calculando periodo de nómina")
    return PayrollPeriodResponse(
        start_date=start_date,
        end_date=end_date,
        year=year,
        month=month
    )

@app.get("/movements/cash_advance/{employee_id}/monthly/{year}/{month}")
def calculate_cash_advance_api(employee_id: int, year: int, month: int):
    calculation = calculate_cash_advance(employee_id, year, month)
    if not calculation:
        raise HTTPException(status_code=500, detail="Error calculando adelantos en caja")

@app.get("/movements/bank-transfer/{employee_id}/monthly/{year}/{month}")
def calculate_bank_transfer_id(employee_id: int, year: int, month: int):
    calculation = calculate_bank_transfer(employee_id, year, month)
    if not calculation:
        raise HTTPException(status_code=500, detail="Error calculando transferencias bancarias")

@app.get("/movements/absence/{employee_id}/monthly/{year}/{month}")
def calculate_absence_discount_api(employee_id: int, year: int, month: int):
    calculation = calculate_absence_discount(employee_id, year, month)
    if not calculation:
        raise HTTPException(status_code=500, detail="Error calculando descuento por faltas injustificadas")

@app.get("/movements/total/{employee_id}/monthly/{year}/{month}")
def calculate_total_discount_api(employee_id: int, year: int, month: int):
    calculation = calculate_total_discount(employee_id, year, month)
    if not calculation:
        raise HTTPException(status_code=500, detail="Error calculando descuento total")
    
@app.get("/payroll-calculation/{year}/{month}", response_model=PayrollCalculationResponse)
def get_payroll_calculation_by_period_api(year: int, month: int):
    start_date, end_date = get_payroll_period(year, month)
    if not start_date or not end_date:
        raise HTTPException(status_code=500, detail="Error calculando período de nómina")
    
    result = get_active_employees_total_salary_this_payroll(start_date, end_date)
    
    if not result["list_net_salaries"]:
        raise HTTPException(status_code=404, detail="No hay empleados activos en este período")
    
    return PayrollCalculationResponse(
        list_net_salaries=result["list_net_salaries"],
        total_to_pay=result["total_to_pay"]
    )

@app.get("/movements/formatted/monthly/{year}/{month}", response_model=List[MovementFormatted])
def get_formatted_movements_api(year: int, month: int):
    df_movements = get_formatted_movements_for_month(year, month)
    if df_movements.empty:
        raise HTTPException(status_code=404, detail="Movimientos no encontrados")
    movements_list = df_movements.to_dict(orient="records")
    return movements_list

@app.get("/movements/formatted/employee/{employee_id}/monthly/{year}/{month}", response_model=List[MovementFormatted])
def get_formatted_movements_for_month_single_employee_api(employee_id: int, year: int, month: int):
    df_movements = get_formatted_movements_for_month_single_employee(employee_id, year, month)
    if df_movements.empty:
        raise HTTPException(status_code=404, detail="Movimientos no encontrados")
    movements_list = df_movements.to_dict(orient="records")
    return movements_list