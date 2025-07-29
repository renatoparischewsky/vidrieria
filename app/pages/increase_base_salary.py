import streamlit as st
from models import Employee

employee_table = Employee.get_all_active()
if employee_table:
    list_employees = [dict(row) for row in employee_table]

selected_employee = st.selectbox(
    "Empleado:",
    options=list_employees,
    format_func=lambda employee: f"{employee['first_name']} {employee['last_name']}"
)

actual_base_salary = selected_employee['base_salary']
st.write(f"## Sueldo actual de {selected_employee['first_name']} {selected_employee['last_name']}: {actual_base_salary:,} CLP")
amount = st.number_input(
    "**SUELDO NUEVO**",
    step=50000,
    min_value=0
)
confirm = st.button("CONFIRMAR")
if confirm:
    if selected_employee and amount > 0:
        employee_id = selected_employee['identifier']
        employee_to_update = Employee()
        employee_to_update.load_employee(employee_id)
        employee_to_update.base_salary = amount
        if employee_to_update.update_employee():
            st.success(f"Sueldo de {employee_to_update.first_name} actualizado a ${amount:,} CLP")
            st.rerun() 
        else:
            st.error("No se pudo actualizar el sueldo en la base de datos.")
    else:
        st.warning("Por favor, selecciona un empleado y un monto válido.")