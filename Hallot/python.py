import json
import sqlite3

# Load department and hall data from JSON files
with open('selected_departments.json', 'r') as f:
    departments = json.load(f)

with open('selected_halls.json', 'r') as f:
    halls = json.load(f)

# Create department mapping
department_mapping = {dept['name']: dept['code'] for dept in departments}

# Fetch students' register numbers from the database
def fetch_students_by_department(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT reg_no FROM students ORDER BY department_code")
    students = cursor.fetchall()
    conn.close()
    
    students_by_dept = {}
    for reg_no in students:
        department_code = reg_no[0][2:5]  # Extracting department code from reg_no
        if department_code not in students_by_dept:
            students_by_dept[department_code] = []
        students_by_dept[department_code].append(reg_no[0])
    
    return students_by_dept

# Allocation algorithm
def allocate_halls(db_path):
    students_by_dept = fetch_students_by_department(db_path)
    hall_allocations = {}

    for hall in halls:
        hall_name = hall['name']
        hall_capacity = hall['capacity']
        hall_allocations[hall_name] = []
        allocated = 0

        for dept_code, students in students_by_dept.items():
            while students and allocated < hall_capacity:
                student = students.pop(0)
                hall_allocations[hall_name].append(student)
                allocated += 1

            if allocated >= hall_capacity:
                break

    return hall_allocations

# Save hall allocations to the database or an output file
def save_allocations(allocations, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS hall_allocations (
                      hall_name TEXT,
                      reg_no TEXT
                    )''')
    
    for hall, students in allocations.items():
        for student in students:
            cursor.execute("INSERT INTO hall_allocations (hall_name, reg_no) VALUES (?, ?)", (hall, student))
    
    conn.commit()
    conn.close()

# Main Function
def main():
    db_path = 'students.db'  # Path to your SQLite database
    allocations = allocate_halls(db_path)
    save_allocations(allocations, db_path)
    print("Hall allocations completed and saved to the database.")

if __name__ == "__main__":
    main()
