import pandas as pd
import openpyxl
import json
import sqlite3
from prettytable import PrettyTable

# Load JSON and Excel data
with open('selected_rooms.json') as f:
    selectedHalls = json.loads(f.read())

# Separate UG and PG register numbers
ug_dict_dept = {"year_1": {}, "year_2": {}, "year_3": {}}
pg_dict_dept = {"year_1": {}, "year_2": {}}

# Department code mappings
department_mapping = {
    "UG_department_codes": {
        "Year 1": {
            "B.Sc. Computer Science": "UCS",
            "B.Sc. Computer Technology": "UCT",
            "B.Sc. Information Technology": "UIT",
            "B.Sc. Computer Science with Graphics and Creative Design": "UGD",
            "B.Sc. Computer Science (AI & DS)": "UAI",
            "B.Sc. CS with Cyber Security": "UCB",
            "B.Sc. CS and Data Analytics": "UDA",
            "B.Sc. CS (DevOps and Cloud)": "UDC",
            "B.Sc. CS (FSWD)": "UFW",
            "B.Sc. CS (Data Science and Visualization)": "UDS",
            "BCA": "UCA",
            "B.Sc. CD&F": "UCD",
            "B.Sc. CS & HM": "UCH",
            "B.Sc. Psychology": "UPY",
            "B.Com.": "UCM",
            "B.Com. DM and DM": "UDM",
            "B.Com. (CA)": "UCC",
            "B.Com. (PA)": "UCP",
            "B.Com. Finance": "UFI",
            "B.Com. (IT)": "UCI",
            "BBA": "UBA",
            "BBA (CA)": "UBC",
            "B.A. English Lit.,": "UEL"
        },
        "Year 2": {
            "B.Sc. Computer Science": "UCS",
            "B.Sc. Computer Technology": "UCT",
            "B.Sc. Information Technology": "UIT",
            "B.Sc. Computer Science with Graphics and Creative Design": "UGD",
            "B.Sc. Computer Science (AI & DS)": "UAI",
            "B.Sc. CS with Cyber Security": "UCB",
            "B.Sc. CS and Data Analytics": "UDA",
            "B.Sc. CS (DevOps and Cloud)": "UDC",
            "B.Sc. CS (FSWD)": "UFW",
            "B.Sc. CS (Data Science and Visualization)": "UDS",
            "BCA": "UCA",
            "B.Sc. CD&F": "UCD",
            "B.Sc. CS & HM": "UCH",
            "B.Sc. Psychology": "UPY",
            "B.Com.": "UCM",
            "B.Com. DM and DM": "UDM",
            "B.Com. (CA)": "UCC",
            "B.Com. (PA)": "UCP",
            "B.Com. Finance": "UFI",
            "B.Com. (IT)": "UCI",
            "BBA": "UBA",
            "BBA (CA)": "UBC",
            "B.A. English Lit.,": "UEL"
        },
        "Year 3": {
            "B.Sc. Computer Science": "BCS",
            "B.Sc. Computer Technology": "BCT",
            "B.Sc. Information Technology": "BIT",
            "B.Sc. Computer Science with Graphics and Creative Design": "BGD",
            "B.Sc. Computer Science (AI & DS)": "BAI",
            "B.Sc. CS with Cyber Security": "BCB",
            "B.Sc. CS and Data Analytics": "BDA",
            "B.Sc. CS (DevOps and Cloud)": "BDC",
            "B.Sc. CS (FSWD)": "BFW",
            "B.Sc. CS (Data Science and Visualization)": "BDS",
            "BCA": "BCA",
            "B.Sc. CD&F": "BCF",
            "B.Sc. CS & HM": "BCH",
            "B.Sc. Psychology": "BPY",
            "B.Com.": "BCM",
            "B.Com. DM and DM": "BDM",
            "B.Com. (CA)": "BCC",
            "B.Com. (PA)": "BCP",
            "B.Com. Finance": "BFI",
            "B.Com. (IT)": "BCI",
            "BBA": "BBA",
            "BBA (CA)": "BAC",
            "B.A. English Lit.,": "BEL"
        }
    },
    "PG_department_codes": {
        "Year 1": {
            "MBA": "PBA",
            "M.COM": "PCM",
            "MCA": "PCA",
            "M.Com (CA)": "PCC",
            "M.A. English Literature": "PEL",
            "M.Sc. Computer Science": "PCS"
        },
        "Year 2": {
            "MBA": "PBA",
            "M.COM": "PCM",
            "MCA": "PCA",
            "M.Com (CA)": "PCC",
            "M.A. English Literature": "PEL",
            "M.Sc. Computer Science": "PCS"
        }
    }
}

# Create a mapping from department code to department name
dept_code_to_name = {}
for year, departments in department_mapping["UG_department_codes"].items():
    for dept_name, dept_code in departments.items():
        dept_code_to_name[dept_code] = dept_name
for year, departments in department_mapping["PG_department_codes"].items():
    for dept_name, dept_code in departments.items():
        dept_code_to_name[dept_code] = dept_name

# Populate the UG and PG dictionaries with data from Excel files
for year, table_name in zip(['2022', '2023', '2024'], ['year_3', 'year_2', 'year_1']):
    df = pd.read_excel(f'{year}_Name_list.xlsx', usecols='C' if year != '2024' else 'B')
    for _, row in df.iterrows():
        reg_num = row.iloc[0]
        reg_year = reg_num[:2]  # Extract the year from the register number
        dept_code = reg_num[2:5]  # Extract department code from register number

        if dept_code.startswith('P'):
            # PG student
            if reg_year == '24':
                pg_dict_dept["year_1"].setdefault(dept_code, []).append(reg_num)
            elif reg_year == '23':
                pg_dict_dept["year_2"].setdefault(dept_code, []).append(reg_num)
        else:
            # UG student
            if reg_year == '24':
                dept_code = 'U' + dept_code[1:]  # Modify dept_code for Year 1
                ug_dict_dept["year_1"].setdefault(dept_code, []).append(reg_num)
            elif reg_year == '23':
                dept_code = 'U' + dept_code[1:]  # Modify dept_code for Year 2
                ug_dict_dept["year_2"].setdefault(dept_code, []).append(reg_num)
            elif reg_year == '22':
                ug_dict_dept["year_3"].setdefault(dept_code, []).append(reg_num)

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
    for dept_code, reg_numbers in data.items():
        dept_name = dept_code_to_name.get(dept_code, "Unknown Department")
        for reg_num in reg_numbers:
            cursor.execute(f'''
                INSERT INTO "{table_name}" ("Department", "Register Number", "Department code")
                VALUES (?, ?, ?)
            ''', (dept_name, reg_num, dept_code))

# Insert the data with department names into the tables
for year in ug_dict_dept.keys():
    create_table(f"UG_{year.capitalize()}")
    insert_data(f"UG_{year.capitalize()}", ug_dict_dept[year])

for year in pg_dict_dept.keys():
    create_table(f"PG_{year.capitalize()}")
    insert_data(f"PG_{year.capitalize()}", pg_dict_dept[year])

# Commit the changes to the database
conn.commit()

# Function to save tables to file using PrettyTable
def save_table_to_file(table_name, file):
    cursor.execute(f'SELECT * FROM "{table_name}"')
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = [description[0] for description in cursor.description]

    for row in rows:
        table.add_row(row)

    file.write(f"Table: {table_name}\n")
    file.write(table.get_string())
    file.write("\n" + "-"*50 + "\n\n")

# Save UG and PG tables to file
tables = [f"UG_{year.capitalize()}" for year in ug_dict_dept.keys()] + [f"PG_{year.capitalize()}" for year in pg_dict_dept.keys()]

with open('Student_table.txt', 'w') as f:
    for table_name in tables:
        save_table_to_file(table_name, f)

# Close the database connection
conn.close()

print("Tables saved to 'students_tables_output.txt' and changes committed to 'students.db'")