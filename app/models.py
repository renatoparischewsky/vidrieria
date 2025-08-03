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
            with sqlite3.connect("db/vidrieria.db") as conn:
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


    def insert_employee(self):
        if self.identifier is not None:
            print("Debes desasignar el id agregado del empleado, de lo contrario no se podrá subir a la base de datos")
            return False
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
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
                return True
        except Exception as e:
            print(f"Error de base de datos: {e}")

    @staticmethod
    def get_all_active():
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT identifier, tax_id, first_name, last_name, base_salary FROM Employee WHERE is_active = 1 ORDER BY last_name")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return []



    @staticmethod
    def get_all_inactive():
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT identifier, tax_id, first_name, last_name, base_salary FROM Employee WHERE is_active = 0 ORDER BY last_name")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return []


    @staticmethod
    def get_all_employees():
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT identifier, tax_id, first_name, last_name, base_salary FROM Employee ORDER BY last_name")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error de base de datos: {e}")
            return []


    def mark_as_inactive(self):
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE Employee SET is_active =  0 WHERE identifier = ?""",
                (self.identifier,)
                )
                conn.commit()
                self.is_active = 0
                return True
        except Exception as e:
            print(f"Error de base de datos: {e}")

    def mark_as_active(self):
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE Employee SET is_active =  1 WHERE identifier = ?""",
                (self.identifier,)
                )
                conn.commit()
                self.is_active = 1
                return True
        except Exception as e:
            print(f"Error de base de datos: {e}")

    def update_employee(self):
        if self.identifier is None:
            return False
        try:
            with sqlite3.connect("db/vidrieria.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Employee 
                    SET tax_id = ?, first_name = ?, last_name = ?, base_salary = ?, is_active = ?
                    WHERE identifier = ?
                """, (
                    self.tax_id, self.first_name, self.last_name, 
                    self.base_salary, self.is_active, self.identifier
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar empleado: {e}")
            return False
