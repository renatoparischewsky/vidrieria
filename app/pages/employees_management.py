import streamlit as st
import pandas as pd
from app.employees import Employee

if 'new_employee' in st.session_state and st.session_state.new_employee:
    st.success(f"Empleado añadido exitosamente")
    st.session_state.new_employee = False

if 'inactivate' in st.session_state and st.session_state.inactivate:
    st.success("Empleado marcado como inactivo con éxito.")
    st.session_state.inactivate = False

if 'activate' in st.session_state and st.session_state.activate:
    st.success("Empleado marcado como activo con éxito.")
    st.session_state.activate = False


add_or_delete = st.sidebar.selectbox(
    'Seleccione si quiere añadir o inactivar a un trabajador',
    ('Añadir', 'Inactivar', 'Activar')
)

if add_or_delete == "Añadir":
    tax_id = st.text_input("Ingrese el RUT del empleado de la forma 12.345.678-9")
    first_name = st.text_input("Ingrese el nombre del empleado")
    last_name = st.text_input("Ingrese el apellido del empleado")
    base_salary = st.text_input("Ingrese el salario base del empleado")
    add_employee = st.button("Añadir")
    if add_employee:
        new_employee = Employee(tax_id, first_name, last_name, base_salary)
        if new_employee.insert_employee():
            st.session_state.new_employee = True
            st.rerun()
        else:
            st.error("No se pudo ingresar al nuevo empleado. Asegurese de añadir un RUT único.")

elif add_or_delete == "Inactivar":
    employee_table = Employee.get_all_active()
    list_employees = [dict(row) for row in employee_table]
    selected_employee = st.selectbox(
        "Empleado:",
        options=list_employees,
        format_func=lambda employee: f"{employee['first_name']} {employee['last_name']}"
    )
    inactivate = st.button("Eliminar (marcar como inactivo debido a despido o por una baja laboral)")

    if inactivate:
        employee_id = selected_employee['employee_id']
        employee_to_inactivate = Employee()
        employee_to_inactivate.load_employee(employee_id)
        if employee_to_inactivate.mark_as_inactive():
            st.session_state.inactivate = True
            st.rerun()
        else:
            st.error("No se pudo actualizar el estado del empleado.")
        

elif add_or_delete == "Activar":
    employee_table = Employee.get_all_inactive()
    list_employees = [dict(row) for row in employee_table]
    selected_employee = st.selectbox(
        "Empleado:",
        options=list_employees,
        format_func=lambda employee: f"{employee['first_name']} {employee['last_name']}"
    )
    activate = st.button("Activar empleado (puede que se haya recontratado o vuelto de una baja)")

    if activate:
        employee_id = selected_employee['employee_id']
        employee_to_activate = Employee()
        employee_to_activate.load_employee(employee_id)
        if employee_to_activate.mark_as_active():
            st.session_state.activate = True
            st.rerun()
        else:
            st.error("No se pudo actualizar el estado del empleado.")
        