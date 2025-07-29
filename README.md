Vidrieria - Personnel & Finance Manager
A personal side-project to build a lightweight system for personnel management and financial movements (absences, advances, transfers, etc.) in my family’s glass-workshop business.

This repo is my attempt to automate the basics while practicing Python, SQLite, creating a web interface with Streamlit, and more. The goal is to create a functional MVP that solves a real-world problem.

🚀 Current Features
The application is built with Streamlit and provides a multi-page dashboard to manage employees and their financial movements.

Employee Dashboard:

View a table of all active employees with their base salary.

Display a real-time calculation of the net salary to be paid for the current month for each employee.

Calculate and display the total liquidity required for the month's payroll.

Movement Management:

Add new movements for any employee, including:

Unjustified Absences (calculates the discount automatically).

Cash Advances.

Bank Transfers.

View a comprehensive list of all movements within a specific month and year.

Delete movements by their unique ID.

Employee Management:

Add new employees to the database.

Deactivate employees (for temporary leave or termination) without deleting their historical data.

Reactivate previously inactive employees.

Update and increase the base salary of any employee.

🛠️ Tech Stack
Backend & Logic: Python

Database: SQLite

Web Interface: Streamlit

Data Manipulation: Pandas

⚙️ Getting Started
Prerequisites
Python 3.x

Git

Installation & Setup
Clone the repository:

Bash

git clone https://github.com/renatoparischewsky/vidrieria.git
cd vidrieria
Create and activate a virtual environment:

Bash

# For Windows
python -m venv .venv
.\.venv\Scripts\activate
Install the required dependencies:

Bash

pip install -r requirements.txt
Initialize the database:
This script will create the vidrieria.db file and the necessary tables if they don't exist.

Bash

python scripts/create_table.py
Running the Application
Once the setup is complete, run the following command to launch the Streamlit application:

Bash

streamlit run app/main.py
Your web browser will open with the application running locally.
