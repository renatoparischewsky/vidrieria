import streamlit as st



project_1_page = st.Page(
    page="pages/employees_dashboard.py",
    title="Tabla Empleados",
    icon=":material/account_circle:",
    default=True
)

project_2_page = st.Page(
    page="pages/discounts_query.py",
    title="Consultar Descuentos",
    icon=":material/account_circle:"
)

project_3_page = st.Page(
    page="pages/movements_management.py",
    title="Añadir o Eliminar Descuento",
    icon=":material/account_circle:"
)

project_4_page = st.Page(
    page="pages/employees_management.py",
    title="Gestionar Trabajadores",
    icon=":material/account_circle:"
)

project_5_page = st.Page(
    page="pages/increase_base_salary.py",
    title="Aumentar Salario",
    icon=":material/account_circle:"
)



pg = st.navigation([project_1_page, project_2_page, project_3_page, project_4_page, project_5_page])


st.title("Sistema de Gestión Vidriería")



pg.run()