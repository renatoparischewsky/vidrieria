from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from datetime import datetime
import re
from datetime import date

# --- EMPLOYEE SCHEMAS ---
class EmployeeBase(BaseModel):
    tax_id: str
    first_name: str
    last_name: str
    base_salary: int

    @field_validator("tax_id")
    @classmethod
    def validate_tax_id_format(cls, v):
        tax_id_pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'

        if not re.match(tax_id_pattern, v):
            raise ValueError(
                "RUT inválido. Use puntos (.) y guión (-)"
            )
        tax_id_validator_separate = v.split("-")
        tax_id_numbers = tax_id_validator_separate[0]
        check_valitador = tax_id_validator_separate[1].upper() # if last digit is k, it will change to K

        tax_id_numbers_clean = int(tax_id_numbers.replace(".", ""))

        if tax_id_numbers_clean < 1 or tax_id_numbers > 99999999:
            raise ValueError(
                "RUT inválido."
            )

        return f"{tax_id_numbers}-{check_valitador}"
    
    @field_validator("base_salary")
    @classmethod
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError("Salario debe ser mayor que 0")
        return v

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeCreate):
    employee_id: int

class EmployeeGet(EmployeeBase):
    employee_id: int
    is_active: bool

class EmployeeUpdate(BaseModel):
    is_active: Optional[bool] = True
    base_salary: Optional[int] = None

# --- MOVEMENT SCHEMAS ---

class MovementBase(BaseModel):
    employee_id: int
    movement_type: str
    amount: int
    date: datetime
    description: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v<= 0:
            raise ValueError("Monto debe ser mayor que 0")
        return v
    
class MovementCreate(MovementBase):
    pass

class MovementGet(MovementBase):
    identifier: int


class BaseMovementRequest(BaseModel):
    employee_id: int
    description: str = ""
    movement_date: date = Field(default_factory=date.today)


class MovementWithAmountRequest(BaseMovementRequest):
    amount: int = Field(..., gt=0, description="El monto debe ser un entero positivo.")

class PayrollPeriodResponse(BaseModel):
    start_date: date
    end_date: date
    year: int
    month: int

class PayrollCalculationResponse(BaseModel):
    list_net_salaries: List[dict]
    total_to_pay: int

class MovementFormatted(BaseModel):
    identifier: int
    employee_id: str  # will be full name with the function get_formatted_movements_for_month
    movement_type: str
    amount: int
    date: str
    description: str = None