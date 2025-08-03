# Vidrieria - Personnel & Finance Manager

A personal side-project to build a **lightweight system** for personnel management and financial movements (absences, advances, transfers, etc.) in my family’s glass-workshop business.

This repo is my attempt to automate the basics while practicing **Python**, **SQLite**, creating a web interface with **Streamlit**, and more. The goal is to create a **functional MVP** that solves a real-world problem.

---

## 🚀 Current Features

### Employee Dashboard
- View a table of all active employees with their **base salary**.
- Display a real-time calculation of the **net salary** to be paid for the current month for each employee.
- Calculate and display the **total liquidity** required for the month's payroll.

### Movement Management
- Add new movements for any employee, including:
  - **Unjustified Absences** (automatic discount calculation).
  - **Cash Advances**.
  - **Bank Transfers**.
- View a comprehensive list of all movements within a specific **month and year**.
- Delete movements by their **unique ID**.

### Employee Management
- Add new employees to the database.
- **Deactivate** employees (for temporary leave or termination) without deleting historical data.
- **Reactivate** previously inactive employees.
- Update and increase the **base salary** of any employee.

---

## 🛠️ Tech Stack
- **Backend & Logic:** Python
- **Database:** SQLite
- **Web Interface:** Streamlit
- **Data Manipulation:** Pandas

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.x
- Git

### Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/renatoparischewsky/vidrieria.git
    cd vidrieria
    ```

2. **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database:**  
   This script will create the `vidrieria.db` file and the necessary tables if they don't exist.
    ```bash
    python scripts/create_table.py
    ```

### Running the Application

Start the Streamlit app with:

```bash
streamlit run app/main.py
