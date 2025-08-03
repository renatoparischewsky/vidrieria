import streamlit as st



project_1_page = st.Page(
    page="pages/employee_dashboard.py",
    title="Tabla Empleados",
    icon=":material/account_circle:",
    default=True
)

project_2_page = st.Page(
    page="pages/net_discounts.py",
    title="Consultar Descuentos",
    icon=":material/account_circle:"
)

project_3_page = st.Page(
    page="pages/insert_movement.py",
    title="Añadir o Eliminar Descuento",
    icon=":material/account_circle:"
)

project_4_page = st.Page(
    page="pages/add_or_delete_employee.py",
    title="Gestionar Trabajadores",
    icon=":material/account_circle:"
)

project_5_page = st.Page(
    page="pages/increase_base_salary.py",
    title="Aumentar Salario",
    icon=":material/account_circle:"
)



pg = st.navigation([project_1_page, project_2_page, project_3_page, project_4_page, project_5_page])

# 3. Añade un título principal a tu aplicación
st.title("Sistema de Gestión Vidriería")


# 4. Ejecuta la página seleccionada
pg.run()