# Vidrieria Personnel & Finance Manager

A personal side-project to build a lightweight system for personnel management and financial movements (absences, advances, transfers, etc.) in my family’s glass-workshop business.

Why am I doing this?
- This is a task that could be highly automatizable, and 
- This repo is my attempt to automate the basics while practising Python, SQLite, creating a web interfase, etc.



Current Status (Sprint 1)

Virtual environment + `pip install pandas sqlite3` | ✅ | Project runs locally in its own venv. 
Basic management of SQL databases and git.
 `Employee` class (Python) | ✅ | Encapsulates id, tax ID, names, salary, active flag. 
 SQLite table `Employee`   | ✅ | Created via `create_table.py` (auto‐generated ID, constraints). 
 Basic CRUD helpers        | ✅ | `insert_employee()` and `load_employee()` tested from a mini *TestModels* script. 

 First commits pushed to GitHub | ✅ | `.db` file ignored, only schema & code tracked. 

So far the code lets me:

1. Spin up `db/vidrieria.db` automatically.  
2. Insert new employees safely (auto-increment id, UNIQUE tax ID).  
3. Load an employee record by id and access its attributes in Python.




```bash
# clone the repo
git clone https://github.com/<your-user>/vidrieria.git
cd vidrieria

# create & activate virtual environment (Windows cmd example)
python -m venv .venv
.\.venv\Scripts\activate

# install runtime deps
pip install -r requirements.txt       # pandas, etc.

# build the local database
python db/create_table.py             # (creates Employee table if missing)

# run quick test
python tests/test_models.py           # inserts & fetches a sample employee
