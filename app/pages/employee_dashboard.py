import streamlit as st
import pandas as pd
from models import Employee
from datetime import datetime
from app.calculations_movement import calculate_total_discount


today = datetime.now()
current_year = today.year
current_month = today.month
months_in_spanish = ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Cctubre","Noviembre","Diciembre")

st.info(f"Mostrando sueldos netos calculados para {months_in_spanish[current_month - 1]} de {current_year}")

employee_table = Employee.get_all_active()

if employee_table:
    data_for_df = []
    total_to_pay = 0
    for emp_row in employee_table:
        employee_data = dict(emp_row)
        net_discount = calculate_total_discount(employee_data['identifier'], current_year, current_month)
        net_salary = employee_data['base_salary'] - net_discount
        employee_data['net_salary'] = net_salary
        data_for_df.append(employee_data)
        total_to_pay += net_salary



    df_employees = pd.DataFrame(data_for_df)


    columns_in_spanish = {
        "identifier": "Identificador",
        "tax_id": "RUT",
        "first_name": "Nombre",
        "last_name":  "Apellido",
        "base_salary": "Sueldo Base",
        'net_salary': "Sueldo Neto"
        }
    

    df_employees = df_employees.rename(columns=columns_in_spanish)
    df_employees = df_employees.set_index("Identificador")

    st.dataframe(df_employees, use_container_width=True)

    st.write(f"# Total a pagar: {total_to_pay:,} CLP")
else:
    st.warning("No hay empleados para mostrar.")
