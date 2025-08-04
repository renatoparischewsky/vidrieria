import streamlit as st
from app.employees import Employee

if 'salary_updated' in st.session_state and st.session_state.salary_updated:
    st.success(f"Sueldo actualizado exitosamente")
    st.session_state.salary_updated = False

employee_table = Employee.get_all_active()
if employee_table:
    list_employees = [dict(row) for row in employee_table]

selected_employee = st.selectbox(
    "Empleado:",
    options=list_employees,
    format_func=lambda employee: f"{employee['first_name']} {employee['last_name']}"
)

actual_base_salary = round(selected_employee['base_salary'])
st.write(f"## Sueldo actual de {selected_employee['first_name']} {selected_employee['last_name']}: {actual_base_salary:,d} CLP")
amount = st.number_input(
    "**SUELDO NUEVO**",
    step=50000,
    min_value=0
)
confirm = st.button("CONFIRMAR")
if confirm:
    if selected_employee and amount > 0:
        employee_id = selected_employee['employee_id']
        employee_to_update = Employee()
        employee_to_update.load_employee(employee_id)
        employee_to_update.base_salary = round(amount)
        if employee_to_update.update_employee():
            st.session_state.salary_updated = True
            st.rerun() 
        else:
            st.error("No se pudo actualizar el sueldo en la base de datos.")
    else:
        st.warning("Por favor, selecciona un empleado y un monto válido.")