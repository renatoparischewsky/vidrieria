CREATE TABLE IF NOT EXISTS employees(
    identifier SERIAL PRIMARY KEY,
    tax_id VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    base_salary NUMERIC(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS movements(
    identifier SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(identifier),
    movement_type VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    date DATE NOT NULL,
    description TEXT
);