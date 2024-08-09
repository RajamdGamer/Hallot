import pandas as pd 

l = [4,11,15,15]
li = {}

def load_selected_halls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

selectedHalls = []
selectedRollNo = []
selectedHalls = load_selected_halls('selected_halls.txt')

df = pd.read_excel('2022_Name List - Deptwise.xlsx',1)

print(df)
def allocation():
    temp_list = []
    currentIndex = 0
    for i in range(0,len(selectedHalls)):
        print(selectedHalls[i])
        li.update({selectedHalls[i] : []})
allocation()
print(li)