import streamlit as st
from datetime import datetime
from models import Employee
from app.calculations_movement import(
    calculate_cash_advance,
    calculate_bank_transfer,
    calculate_absence_discount,
    calculate_total_discount,
    get_formatted_movements_for_month_single_employee
)



st.write("Consulta de Descuentos por Empleado")

st.sidebar.header("Filtros de Búsqueda")

employees = Employee.get_all_active()

if employees:
    list_employees = [dict(row) for row in employees]

selected_employee = st.sidebar.selectbox(
    "Empleado:",
    options=list_employees,
    format_func=lambda employee: f"{employee['first_name']} {employee['last_name']}"
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

month_selected_number = months.index(month_selected_word) + 1


employee_id = selected_employee["identifier"]

st.subheader(f"Resultados para: {selected_employee['first_name']} {selected_employee['last_name']}")
st.divider()
discount = calculate_cash_advance(employee_id, year_selected, month_selected_number)
st.metric(label="**Total Adelantos en Caja**", value=f"${discount:,d} CLP")
st.divider()
discount = calculate_bank_transfer(employee_id, year_selected, month_selected_number)
st.metric(label="**Total Transferencias**", value=f"${discount:,d} CLP")
st.divider()
discount = calculate_absence_discount(employee_id, year_selected, month_selected_number)
st.metric(label="**Total Faltas Injustificadas**", value=f"${discount:,d} CLP")
st.divider()
discount = calculate_total_discount(employee_id, year_selected, month_selected_number)
st.metric(label="**Descuento Total del Mes**", value=f"${discount:,d} CLP")
    
    
df_movements = get_formatted_movements_for_month_single_employee(employee_id, year_selected, month_selected_number)


columns_in_spanish = {
"identifier": "ID",
"employee_id": "Trabajador",
"movement_type": "Tipo de Movimiento",
"amount":  "Monto",
"date": "Fecha",
"description": "Descripción"
}

if df_movements.empty:
    pass
else:
    df_movements = df_movements.rename(columns=columns_in_spanish)
    df_movements = df_movements.set_index("ID")
    st.dataframe(df_movements, use_container_width=True)