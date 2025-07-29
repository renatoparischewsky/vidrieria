from app.models_movements import Movement
from app.models import Employee
from datetime import date

def register_cash_advance(employee_id: int, amount: int, description: str = "", movement_date: str = None):
    if movement_date == None:
        movement_date = date.today().isoformat()

    advance = Movement(
        employee_id=employee_id,
        movement_type="CASH_ADVANCE",
        amount=amount,
        date=movement_date,
        description=description
    )

    return advance.insert_movement()

def register_bank_transfer(employee_id: int, amount: int, description: str = "", movement_date: str = None):
    if movement_date == None:
        movement_date = date.today().isoformat()

    advance = Movement(
        employee_id=employee_id,
        movement_type="BANK_TRANSFER",
        amount=amount,
        date=movement_date,
        description=description
    )

    return advance.insert_movement()

def register_abscence(employee_id: int, description: str = "", movement_date: str = None):
    if movement_date == None:
        movement_date = date.today().isoformat()

    employee = Employee()
    employee.load_employee(employee_id)
    daily_discount = round(employee.base_salary / 30)

    advance = Movement(
        employee_id=employee_id,
        movement_type="UNJUSTIFIED_ABSENCE",
        amount=daily_discount,
        date=movement_date,
        description=description
    )
    
    return advance.insert_movement()

def calculate_cash_advance(employee_id: int, year: int, month: int):
    movements = Movement.find_by_employee_and_month(employee_id, year, month)

    total_discount = 0
    for movement in movements:
        if movement["movement_type"] == "CASH_ADVANCE":
            total_discount += movement["amount"]

    return total_discount

def calculate_bank_transfer(employee_id: int, year: int, month: int):
    movements = Movement.find_by_employee_and_month(employee_id, year, month)

    total_discount = 0
    for movement in movements:
        if movement["movement_type"] == "BANK_TRANSFER":
            total_discount += movement["amount"]

    return total_discount

def calculate_absence_discount(employee_id: int, year: int, month: int):
    employee = Employee()
    if not employee.load_employee(employee_id):
        print(f"Error: no se pudo cargar o no existe el empleado con ID {employee_id}")
        return 0
    if not employee.base_salary or employee.base_salary <= 0:
        print("No hay sueldo para descontar")
        return 0
    
    movements = Movement.find_by_employee_and_month(employee_id, year, month)

    absence_count = 0
    for movement in movements:
        if movement["movement_type"] == "UNJUSTIFIED_ABSENCE":
            absence_count += 1

    daily_value = employee.base_salary/30
    total_discount = daily_value * absence_count
    return round(total_discount)

def calculate_total_discount(employee_id: int, year: int, month: int):
    employee = Employee()
    if not employee.load_employee(employee_id):
        print(f"No se pudo encontrar un trabajador con ID {employee_id}")
        return
    
    total_discount = calculate_cash_advance(employee_id, year, month) + calculate_bank_transfer(employee_id, year, month) + calculate_absence_discount(employee_id, year, month)
    
    return round(total_discount)
