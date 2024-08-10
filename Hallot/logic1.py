import pandas as pd 
import openpyxl
import json
import sqlite3
from prettytable import PrettyTable

# Load JSON and Excel data
f = open('selected_rooms.json')
selectedHalls = json.loads(f.read())
selectedRollNo = []

# Load and process Excel files for each year
for year in ['2022', '2023', '2024']:
    wb = openpyxl.load_workbook(f'{year}_Name_list.xlsx')
    df = pd.read_excel(f'{year}_Name_list.xlsx', usecols='C' if year != '2024' else 'B')
    for _, row in df.iterrows():
        reg = row
        selectedRollNo.append(reg.item())

# Separate UG and PG register numbers
ug_dict_dept = {"year 1": {}, "year 2": {}, "year 3": {}}
pg_dict_dept = {"year 1": {}, "year 2": {}}

# Loop through each department identifier in 'selectedRollNo'
for reg_no in selectedRollNo:
    if reg_no == 'nan':
        continue
    
    dept_code = str(reg_no)[2:5]
    year_prefix = str(reg_no)[0:2]
    
    if dept_code.startswith("P"):
        # PG Register Numbers
        if year_prefix == "23":
            pg_dict_dept["year 2"].setdefault(dept_code, []).append(reg_no)
        elif year_prefix == "24":
            pg_dict_dept["year 1"].setdefault(dept_code, []).append(reg_no)
    else:
        # UG Register Numbers
        if year_prefix == "22":
            ug_dict_dept["year 3"].setdefault(dept_code, []).append(reg_no)
        elif year_prefix == "23":
            ug_dict_dept["year 2"].setdefault(dept_code, []).append(reg_no)
        elif year_prefix == "24":
            ug_dict_dept["year 1"].setdefault(dept_code, []).append(reg_no)

# Connect to SQLite database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Function to create a table for a specific year
def create_table(table_name):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            "S. No." INTEGER PRIMARY KEY AUTOINCREMENT,
            "Department" TEXT,
            "Register Number" TEXT,
            "Department code" TEXT
        )
    ''')

# Function to insert data into the table
def insert_data(table_name, data):
    for dept, reg_numbers in data.items():
        for reg_num in reg_numbers:
            cursor.execute(f'''
                INSERT INTO "{table_name}" ("Department", "Register Number", "Department code")
                VALUES (?, ?, ?)
            ''', (dept, reg_num, dept))

# Create UG and PG tables and insert data
for year in ug_dict_dept.keys():
    create_table(f"UG_{year.capitalize()}")
    insert_data(f"UG_{year.capitalize()}", ug_dict_dept[year])

for year in pg_dict_dept.keys():
    create_table(f"PG_{year.capitalize()}")
    insert_data(f"PG_{year.capitalize()}", pg_dict_dept[year])

# Commit the changes and close the connection
conn.commit()
conn.close()

# Function to save tables to file using PrettyTable
def save_table_to_file(table_name, file):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM "{table_name}"')
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = [description[0] for description in cursor.description]

    for row in rows:
        table.add_row(row)

    file.write(f"Table: {table_name}\n")
    file.write(table.get_string())
    file.write("\n" + "-"*50 + "\n\n")

    conn.close()

# Save UG and PG tables to file
tables = [f"UG_{year.capitalize()}" for year in ug_dict_dept.keys()] + [f"PG_{year.capitalize()}" for year in pg_dict_dept.keys()]

with open('students_tables_output.txt', 'w') as file:
    for table in tables:
        save_table_to_file(table, file)

print("Tables saved to 'students_tables_output.txt'")
