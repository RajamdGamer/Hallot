import json
import sqlite3
import random

# Load department and hall data from JSON files
with open('selected_departments.json', 'r') as f:
    departments = json.load(f)

with open('selected_rooms.json', 'r') as f:
    selected_halls_from_json = json.load(f)

# Create department mapping
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
            "B.A. English Lit.": "UEL"
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
            "B.A. English Lit.": "UEL"
        },
        "Year 3": {
            "B.Sc. Computer Science": "BCS",
            "B.Sc. Computer Technology": "BCT",
            "B.Sc. Information Technology": "BIT",
            "B.Sc. Computer Science with Graphics and Creative Design": "BGD",
            "B.Sc. Computer Science (AI & DS)": "BAI",
            "B.Sc. CS with Cyber Security": "BCB",
            "B.Sc. CS and Data Analytics": "BDA",
            "B.Sc. CS (DevOps and Cloud)": "UDC",
            "B.Sc. CS (FSWD)": "UFW",
            "B.Sc. CS (Data Science and Visualization)": "UDS",
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
            "B.A. English Lit.": "BEL"
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

# Sample halls data (replace this with actual data or load from a JSON file)
halls = [
    {'name': 'A-204', 'capacity': 45},
    {'name': 'A-205', 'capacity': 35},
    {'name': 'A-208', 'capacity': 45},
    {'name': 'A-209', 'capacity': 45},
    {'name': 'A-210', 'capacity': 45},
    {'name': 'A-211', 'capacity': 42},
    {'name': 'A-301', 'capacity': 44},
    {'name': 'A-303', 'capacity': 45},
    {'name': 'A-304', 'capacity': 45},
    {'name': 'A-305', 'capacity': 45},
    {'name': 'A-306', 'capacity': 45},
    {'name': 'A-308', 'capacity': 38},
    {'name': 'A-309', 'capacity': 45},
    {'name': 'A-310', 'capacity': 42},
    {'name': 'A-311', 'capacity': 42},
    {'name': 'A-312', 'capacity': 45},
    {'name': 'B-101', 'capacity': 42},
    {'name': 'B-104', 'capacity': 45},
    {'name': 'B-109', 'capacity': 33},
    {'name': 'B-207', 'capacity': 45},
    {'name': 'B-208', 'capacity': 45},
    {'name': 'B-211', 'capacity': 33},
    {'name': 'B-212', 'capacity': 36},
    {'name': 'B-302', 'capacity': 45},
    {'name': 'C-104', 'capacity': 35},
    {'name': 'C-105', 'capacity': 45},
    {'name': 'C-107', 'capacity': 45},
    {'name': 'C-108', 'capacity': 45},
    {'name': 'C-109', 'capacity': 45},
    {'name': 'C-110', 'capacity': 45},
    {'name': 'C-205', 'capacity': 42},
    {'name': 'C-206', 'capacity': 45},
    {'name': 'C-207', 'capacity': 45},
    {'name': 'D-002', 'capacity': 45},
    {'name': 'D-005', 'capacity': 45},
    {'name': 'D-104', 'capacity': 45},
    {'name': 'D-105', 'capacity': 45},
    {'name': 'D-201', 'capacity': 45},
    {'name': 'D-202', 'capacity': 45},
    {'name': 'E-002', 'capacity': 45},
    {'name': 'E-003', 'capacity': 42},
    {'name': 'E-004', 'capacity': 45},
    {'name': 'E-005', 'capacity': 45},
    {'name': 'E-006', 'capacity': 42},
    {'name': 'E-101', 'capacity': 45},
    {'name': 'E-102', 'capacity': 45},
    {'name': 'E-103', 'capacity': 45},
    {'name': 'E-105', 'capacity': 42},
    {'name': 'E-201', 'capacity': 45},
    {'name': 'E-202', 'capacity': 45},
    {'name': 'E-203', 'capacity': 45},
    {'name': 'E-205', 'capacity': 45},
    {'name': 'E-206', 'capacity': 45},
    {'name': 'E-301', 'capacity': 45},
    {'name': 'E-302', 'capacity': 45},
    {'name': 'E-303', 'capacity': 45},
    {'name': 'E-305', 'capacity': 45},
    {'name': 'E-306', 'capacity': 45},
    {'name': 'E-307', 'capacity': 45},
    {'name': 'F-201', 'capacity': 45},
    {'name': 'F-202', 'capacity': 30},
    {'name': 'F-203', 'capacity': 40},
    {'name': 'F-301', 'capacity': 45},
    {'name': 'F-302', 'capacity': 45},
    {'name': 'F-303', 'capacity': 45},
    {'name': 'CS-201', 'capacity': 45},
    {'name': 'CS-202', 'capacity': 45},
    {'name': 'CS-203', 'capacity': 42},
    {'name': 'CS-204', 'capacity': 45},
    {'name': 'CS-205', 'capacity': 45},
    {'name': 'CS-301', 'capacity': 45}
]


def fetch_students_by_department_and_year(db_path, selected_departments):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    table_mapping = {
        "1": {"UG": "UG_Year_1", "PG": "PG_Year_1"},
        "2": {"UG": "UG_Year_2", "PG": "PG_Year_2"},
        "3": {"UG": "UG_Year_3"}
    }

    students_by_dept = {}

    for dept_name, years in selected_departments.items():
        dept_code = None
        level = None

        for year in ["Year 1", "Year 2", "Year 3"]:
            dept_code = department_mapping["UG_department_codes"].get(year, {}).get(dept_name)
            if dept_code:
                level = "UG"
                break

        if not dept_code:
            for year in ["Year 1", "Year 2"]:
                dept_code = department_mapping["PG_department_codes"].get(year, {}).get(dept_name)
                if dept_code:
                    level = "PG"
                    break

        if not dept_code:
            print(f"Department code not found for {dept_name}")
            continue

        students_by_dept[dept_code] = []

        for year in years:
            table_name = table_mapping[year].get(level)
            if not table_name:
                print(f"No table mapping found for year {year} and level {level}")
                continue

            query = f"SELECT 'Register Number' FROM {table_name} WHERE 'Department code' = ?"
            cursor.execute(query, (dept_code,))
            students = cursor.fetchall()
            students_by_dept[dept_code].extend([student[0] for student in students])

    conn.close()
    return students_by_dept

def randomize_batches(students, num_batches=4):
    if not students:
        return []

    random.shuffle(students)
    batch_sizes = []
    remaining_students = len(students)

    for _ in range(num_batches - 1):
        max_batch_size = remaining_students - (num_batches - len(batch_sizes) - 1)
        if max_batch_size <= 0:
            break
        batch_size = random.randint(1, max_batch_size)
        batch_sizes.append(batch_size)
        remaining_students -= batch_size

    if remaining_students > 0:
        batch_sizes.append(remaining_students)

    return batch_sizes

def allocate_halls(db_path, selected_halls, selected_depts):
    students_by_dept = fetch_students_by_department_and_year(db_path, selected_depts)
    hall_allocations = {}

    total_students = sum(len(students) for students in students_by_dept.values())
    total_capacity = sum(hall['capacity'] for hall in selected_halls)

    if total_students > total_capacity:
        print(f"Warning: Not enough capacity! You need {total_students - total_capacity} more seats.")
        return None

    available_halls = list(selected_halls)
    random.shuffle(available_halls)

    for hall in available_halls:
        hall_name = hall['name']
        hall_capacity = hall['capacity']
        hall_allocations[hall_name] = []
        hall_capacity_left = hall_capacity

        for dept_code, students in students_by_dept.items():
            if not students:
                continue

            batches = randomize_batches(students, num_batches=4)

            for batch_size in batches:
                if batch_size <= hall_capacity_left:
                    hall_allocations[hall_name].extend(students[:batch_size])
                    students = students[batch_size:]
                    hall_capacity_left -= batch_size
                else:
                    hall_allocations[hall_name].extend(students[:hall_capacity_left])
                    students = students[hall_capacity_left:]
                    break

                if hall_capacity_left <= 0:
                    break

            if hall_capacity_left <= 0:
                break

    return hall_allocations

# Main execution
db_path = 'students.db'
selected_halls = [hall for hall in halls if hall['name'] in selected_halls_from_json]
selected_depts = departments

allocations = allocate_halls(db_path, selected_halls, selected_depts)
if allocations:
    with open('hall_allocations.txt', 'w') as f:
        for hall, students in allocations.items():
            f.write(f"HALL: {hall}\n")
            for student in students:
                f.write(f"{student}\n")
            f.write("\n")
    print("Hall allocations have been written to 'hall_allocations.txt'.")
else:
    print("Allocation failed.")

