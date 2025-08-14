from app.movements import Movement
from app.employees import Employee
from datetime import date, timedelta
import holidays
import calendar
import pandas as pd

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

    employee = Employee.load_employee(employee_id)
    daily_discount = round(employee.base_salary / 30)

    advance = Movement(
        employee_id=employee_id,
        movement_type="UNJUSTIFIED_ABSENCE",
        amount=daily_discount,
        date=movement_date,
        description=description
    )
    
    return advance.insert_movement()

def get_payment_date(year: int, month: int):
    chile_holidays = holidays.Chile(years=year)
    if month == 2:
        total_days = calendar.monthrange(year, month)[1]
    else:
        total_days = 30
    date_to_pay = date(year, month, total_days)
    while date_to_pay.weekday() >= 5 or date_to_pay in chile_holidays:
        date_to_pay -= timedelta(days=1)
    return date_to_pay

def get_payroll_period(year: int, month: int) -> tuple[date,date]:
    end_date = get_payment_date(year, month)
    
    previous_month_year = year if month > 1 else year - 1
    previous_month_month = month - 1 if month > 1 else 12
    start_date = get_payment_date(previous_month_year, previous_month_month) + timedelta(days=1)

    return start_date, end_date

def calculate_cash_advance(employee_id: int, year: int, month: int):
    movements = Movement.find_by_employee_and_month(employee_id, year, month)

    total_discount = 0
    for movement in movements:
        if movement["movement_type"] == "CASH_ADVANCE":
            total_discount += movement["amount"]

    return round(total_discount)

def calculate_bank_transfer(employee_id: int, year: int, month: int):
    movements = Movement.find_by_employee_and_month(employee_id, year, month)

    total_discount = 0
    for movement in movements:
        if movement["movement_type"] == "BANK_TRANSFER":
            total_discount += movement["amount"]

    return round(total_discount)

def calculate_absence_discount(employee_id: int, year: int, month: int):
    employee = Employee()
    if not employee.load_employee(employee_id):
        print(f"Error: no se pudo cargar o no existe el empleado con ID {employee_id}")
        return 0
    
    movements = Movement.find_by_employee_and_month(employee_id, year, month)

    total_discount = 0
    for movement in movements:
        if movement["movement_type"] == "UNJUSTIFIED_ABSENCE":
            total_discount += movement["amount"]

    return round(total_discount)

def calculate_total_discount(employee_id: int, year: int, month: int):
    employee = Employee()
    if not employee.load_employee(employee_id):
        print(f"No se pudo encontrar un trabajador con ID {employee_id}")
        return
    
    total_discount = calculate_cash_advance(employee_id, year, month) + calculate_bank_transfer(employee_id, year, month) + calculate_absence_discount(employee_id, year, month)
    
    return total_discount


def get_active_employees_total_salary_this_payroll(start_date, end_date):
    employees = Employee.get_all_active()
    if not employees:
        return {"list_net_salaries": [], "total_to_pay": 0}
    list_net_salaries = []
    total_to_pay = 0
    for emp_row in employees:
        employee_data = dict(emp_row)
        employee_id = employee_data['employee_id']
        movements = Movement.find_by_employee_and_date_range(employee_id, start_date, end_date)
        total_discount = round(sum(mov['amount'] for mov in movements))
        base_salary = employee_data['base_salary']
        net_salary = base_salary - total_discount
        employee_data['base_salary'] = round(base_salary)
        employee_data['net_salary'] = round(net_salary)
        list_net_salaries.append(employee_data)
        total_to_pay += net_salary
    return {
        "list_net_salaries": list_net_salaries,
        "total_to_pay": round(total_to_pay)
    }