import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from models import Employee
from calculations_movement import(
    calculate_cash_advance,
    calculate_bank_transfer,
    calculate_absence_discount,
    calculate_total_discount
)

st.write("Consulta de Descuentos por Empleado")

st.sidebar.header("Filtros de Búsqueda")

type_discount = st.sidebar.selectbox(
    '¿Qué descuentos te gustaría ver?',
    ('Adelantos en caja', 'Transferencias', 'Faltas Injustificadas', 'Todos'),
    key='discounts'
)
today = datetime.now()
year_selected = st.sidebar.number_input(
    "Año:",
    value=today.year)


months = ('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')
month_selected_word = st.sidebar.selectbox(
    'Mes',
    months,
    index=today.month - 1
)


employee_table = Employee.get_all_active()
if employee_table:
    list_employees = [dict(row) for row in employee_table]

selected_employee = st.sidebar.selectbox(
    "Empleado:",
    options=list_employees,
    format_func=lambda employee: f"{employee['first_name']} {employee['last_name']}"
)


if st.sidebar.button("Calcular"):
    employee_id = selected_employee["identifier"]
    month_selected_number = months.index(month_selected_word) + 1


    st.subheader(f"Resultados para: {selected_employee['first_name']} {selected_employee['last_name']}")
        
    if type_discount == "Adelantos en caja":
        st.divider()
        discount = calculate_cash_advance(employee_id, year_selected, month_selected_number)
        st.metric(label="Total Adelantos en Caja", value=f"${discount}")
        

    elif type_discount == "Transferencias":
        st.divider()
        discount = calculate_bank_transfer(employee_id, year_selected, month_selected_number)
        st.metric(label="Total Transferencias", value=f"${discount}")
        
    
    elif type_discount == "Faltas Injustificadas":
        st.divider()
        discount = calculate_absence_discount(employee_id, year_selected, month_selected_number)
        st.metric(label="Total Faltas Injustificaas", value=f"${discount}")
        
    
    
    elif type_discount == "Todos":
        st.divider()
        discount = calculate_total_discount(employee_id, year_selected, month_selected_number)
        st.metric(label="**Descuento Total del Mes**", value=f"${discount}")
    else:
        st.warning("No hay empleados para mostrar o seleccionar.")


