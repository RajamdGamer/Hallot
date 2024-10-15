import pandas as pd
import openpyxl
import random

students = [] # input - 1

for year in ['2022', '2023', '2024']:
    wb = openpyxl.load_workbook('2023_Name List.xlsx')
    df = pd.read_excel(f'2023_Name List.xlsx', usecols='C' if year != '2024' else 'B')
    for _, row in df.iterrows():
        reg = row
        students.append(reg.item())
# input - 2
selectedhalls = ["B101", "B104", "B107", "B109", "B203", "B205", "B207", "B208", "B209", "B210", "B211", "B212", "B302"]
output = [] # - output.
        #[[0],[1],[2],[3],[4],[5],[6],[7]]    
for i in selectedhalls:
    output.append([i])
    
def randomSet():
    res = []
    splitters = [15,8,3,1]
    x = splitters[0]
    
    sublists = []
    for i in students:
        print()
    print(students)

        

    
    
    
randomSet()    

File_object = open(r"output.txt","w")
File_object.writelines(str(output))

File_object.close()
