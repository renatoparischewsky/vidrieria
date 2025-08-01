import streamlit as st
import pandas as pd
from datetime import datetime
from app.models_movements import Movement
from app.models import Employee


if 'current_movements' not in st.session_state:
    st.session_state.current_movements = None

type_movement = st.sidebar.selectbox(
    'Seleccione si quiere añadir o eliminar un moviemiento',
    ('Añadir', 'Eliminar'),
    key='movements'
)

if type_movement == 'Añadir':
    st.write("""
    ### Indicaciones: Elija el tipo de descuento, a cuál empleado le corresponde y el monto. Si el tipo de descuento es "Falta Injustificada" el monto que se descuenta se calcula internamente, por lo que no debe añadir manualmente el monto.        
    """)

    type_discount_map = {
    "Adelantos en Caja": "CASH_ADVANCE",
    "Transferencia": "BANK_TRANSFER",
    "Falta Injustificada": "UNJUSTIFIED_ABSENCE"
    }
    type_discount = st.sidebar.selectbox(
        'Seleccione el tipo de descuento',
        ('Falta Injustificada', 'Adelantos en Caja', 'Transferencia')
    )


    date_selected = st.date_input(
        "Fecha del Movimiento:",
        value=datetime.now()
    )
    st.write("Fecha seleccionada:", date_selected)

    employee_table = Employee.get_all_active()
    list_employees = [dict(row) for row in employee_table]
    selected_employee = st.sidebar.selectbox(
        "Empleado:",
        options=list_employees,
        format_func=lambda employee: f"{employee['first_name']} {employee['last_name']}"
    )
    if type_discount == "Adelantos en Caja" or type_discount == "Transferencia":
        amount = st.sidebar.number_input(
            "Monto",
            step=25000,
            min_value=0
        )
    else:
        employee = Employee()
        employee_id = selected_employee['identifier']
        employee.load_employee(employee_id)
        amount = round(employee.base_salary / 30)



    description = st.text_input("Añada una descripción (opcional)")

    if st.sidebar.button("Añadir movimiento"):
        employee_id = selected_employee["identifier"]
        movement_type = type_discount_map[type_discount]
        date = date_selected.isoformat()
        added_movement = Movement(employee_id, movement_type, amount, date, description)
        if added_movement.insert_movement():
            st.info("Movimiento añadido exitosamente")
        

if type_movement == 'Eliminar':
    st.sidebar.write("Selecciona el período a consultar:")
    st.write("""
    ### Indicaciones: Primero debe escribir el número de ID que desee eliminar, apretar ENTER y después presionar "Eliminar Movimiento Seleccionado".
    """)
    today = datetime.now()

    months = ('Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre')

    month_selected_word = st.sidebar.selectbox(
        'Mes:',
        months,
        index=today.month - 1  
    )
    month_selected_number = months.index(month_selected_word) + 1

    year_selected = st.sidebar.number_input(
        'Año:',
        value=today.year
    )
    
    st.subheader("Movimientos del Período")
    movements = Movement.find_by_month(year_selected, month_selected_number)
    if not movements:
        st.info("No se encontraron movimientos para el período seleccionado.")
    else:
        df_movements = pd.DataFrame([dict(row) for row in movements])
        employees_list = Employee.get_all_active()
        employee_mapping = {emp['identifier']: f"{emp['first_name']} {emp['last_name']}" for emp in employees_list}
        df_movements['employee_id'] = df_movements['employee_id'].map(employee_mapping)
        movement_type_map = {
            "CASH_ADVANCE": "Adelanto en Caja",
            "BANK_TRANSFER": "Transferencia",
            "UNJUSTIFIED_ABSENCE": "Falta Injustificada"
        }
        df_movements['movement_type'] = df_movements['movement_type'].map(movement_type_map)
        columns_in_spanish = {
            "identifier": "ID",
            "employee_id": "Trabajador",
            "movement_type": "Tipo de Movimiento",
            "amount":  "Monto",
            "date": "Fecha",
            "description": "Descripción"
        }
        df_movements = df_movements.rename(columns=columns_in_spanish)
        mov_to_delete = st.number_input(
            "Selecciona el ID del movimiento que quieres eliminar:",
            min_value=1,
            step=None,
            key="id_to_delete"
        )
        df_movements = df_movements.set_index("ID")
        st.dataframe(df_movements, use_container_width=True)
        st.session_state['movements_data'] = df_movements
        st.subheader("Eliminar un Movimiento")
        if st.button("Eliminar Movimiento Seleccionado", type="primary"):
            if Movement.delete_by_id(mov_to_delete):
                st.rerun()