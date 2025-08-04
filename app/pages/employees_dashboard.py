import streamlit as st
import pandas as pd
from datetime import datetime
from app.calculations_movement import get_active_employees_total_salary_this_payroll, get_payroll_period


today = datetime.now()
start_date, end_date = get_payroll_period(today.year, today.month)

st.info(f"Mostrando sueldos netos para el período de pago: {start_date.strftime('%d/%m/%Y')} al {end_date.strftime('%d/%m/%Y')}")

employee_net_salaries_and_total_to_pay = get_active_employees_total_salary_this_payroll(start_date, end_date)

list_net_salaries = employee_net_salaries_and_total_to_pay["list_net_salaries"]
df_employees = pd.DataFrame(list_net_salaries)

columns_in_spanish = {
    "employee_id": "ID",
    "tax_id": "RUT",
    "first_name": "Nombre",
    "last_name":  "Apellido",
    "base_salary": "Sueldo Base",
    'net_salary': "Sueldo Neto"
    }

df_employees = df_employees.rename(columns=columns_in_spanish)
df_employees = df_employees.set_index("ID")
st.dataframe(df_employees, use_container_width=True)

total_to_pay = employee_net_salaries_and_total_to_pay["total_to_pay"]
st.metric(label="Liquidez Total Necesaria para este Mes", value=f"${total_to_pay:,.0f} CLP")
