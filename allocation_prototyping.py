import pandas as pd
import openpyxl
import random

students = [] # input - 1

for year in ['2022', '2023', '2024']:
    wb = openpyxl.load_workbook(f'{year}_Name_list.xlsx')
    df = pd.read_excel(f'{year}_Name_list.xlsx', usecols='C' if year != '2024' else 'B')
    for _, row in df.iterrows():
        reg = row
        students.append(reg.item())
# input - 2
selectedhalls = ["B101", "B104", "B107", "B109", "B203", "B205", "B207", "B208", "B209", "B210", "B211", "B212", "B302"]
output = [] # - output.
        #[[0],[1],[2],[3],[4],[5],[6],[7]]    
for i in selectedhalls:
    output.append([i])
    
print(students)
def randomSet():
    res = []
    splitters = [15,15,12,3,11,4]
    x = splitters[0]
    
    sublists = []

    for i in range(0, len(students),x):
        sublists.append(students[i:i+x])
        for j in range(0, )
        rand = random.randint(1,5)
        x = splitters[rand]
    
    # sublists = [students[i:i+x] for i in range(0, len(students),x)]
    
    
    for i in range(0,len(output)):
      output[i].append(sublists[i])
    
randomSet()    

File_object = open(r"output.txt","w")
File_object.writelines(str(output))

File_object.close()
