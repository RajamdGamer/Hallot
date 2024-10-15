import pandas as pd 
import openpyxl
import json
l = [4,11,15,15]
li = []


f = open('selected_rooms.json')
selectedHalls = json.loads(f.read())
print(selectedHalls)
selectedRollNo = []

output = {"A204 " : [["22BIT001"],["22BIT003"],["22BIT005"],["22BIT006"]], "A205" : [["22BAI002"],["22BAI004"],["22BAI006"],["22BAI008"]]}

df = pd.read_excel('2022_Name List - Deptwise.xlsx')
print(df)
#for _, row in df.iterrows():
 #   register_number = row['Register #']
  #  
   # selectedRollNo.append(register_number)
output.update({"206": [["22Bai0034"],["22Bai0045"]]})

for x, y in output.items():
  print(x, y)

print(li)
def allocation():
    temp_list = []
    currentIndex = 0
    for i in range(0,len(selectedHalls)):
        print(selectedHalls[i])
        output.update({selectedHalls[i] : []})
allocation()
print(output)