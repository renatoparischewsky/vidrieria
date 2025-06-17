import sqlite3

class Employee:
    def __init__(self, tax_id=None, first_name=None, last_name=None, base_salary=None, is_active: int = 1, identifier=None):
        self.identifier = identifier
        self.tax_id = tax_id
        self.first_name = first_name
        self.last_name = last_name
        self.base_salary = base_salary
        self.is_active = is_active

    def load_employee(self, identifier):
        try:
            conn = sqlite3.connect("db/vidreria.db")
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM Employee                    
            WHERE identifier = ?                    
            """, (identifier,)) # the comma after the variable identifier is because I need to input a tuple as an argument, and without the comma is just an expression with brackets

            row = cursor.fetchone()
            if row is None: # So, there was no record found.
                print(f"Empleado con id {identifier} no existe actualmente.")
                return False
            self.identifier = row[0]
            self.tax_id = row[1]
            self.first_name = row[2]
            self.last_name = row[3]
            self.base_salary = row[4]
            self.is_active = row[5]
            return True
        except Exception as e:
            print("Error inesperado.")
        finally:
            conn.close()

    def insert_employee(self):
        if self.identifier is not None:
            print("Debes desasignar el id agregado del empleado, de lo contrario no se podrá subir a la base de datos")
            return False
        conn = sqlite3.connect("db/vidreria.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO Employee (tax_id, first_name, last_name, base_salary, is_active)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            self.tax_id,
            self.first_name,
            self.last_name, 
            self.base_salary,
            self.is_active)
        )

        self.identifier = cursor.lastrowid

        conn.commit()
        conn.close()
