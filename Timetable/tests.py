from django.test import TestCase
from pathlib import Path
import re
import os
import numpy as np
import pandas as pd
import xlsxwriter

data = 'Course No	Course Name	Slot	Category	Type HS3180 	Decentralization and Governance	J 	Humanities               	ELEC       CH3521	Heat and MAss Transfer Lab II	Q 	Professional             	CORE       CH3021	CRE LAB	P 	Professional             	CORE       CH3052	Material Science for Chemical Engineers	A 	Professional             	CORE       CH3050	Process Dynamics and Control	D 	Professional             	CORE       CH5027	Principles of Thermal Processing and Packaging in Food Industries	K 	Science                  	ELEC      '
text = re.split(r'\s+', data)
start = 0
for idx, i in enumerate(text):
    if len(i) == 6 and i[:2].isalpha() and i[2:].isdigit():
        start = idx
        break
tx_list = text[idx:]
tt = {}
flag = 0
key = val = ''
for i in range(len(tx_list) - 1):
    if flag == 0:
        if len(tx_list[i]) == 6 and tx_list[i][:2].isalpha() and tx_list[i][2:].isnumeric():
            val = tx_list[i]
        elif len(tx_list[i]) == 1 and (
                tx_list[i + 1] == "Science" or tx_list[i + 1] == "Professional" or tx_list[
            i + 1] == "Engineering" or
                tx_list[i + 1] == "Humanities"):
            key = tx_list[i]
            flag = 1
    if flag == 1:
        tt[key] = val
        flag = 0
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(os.path.join(BASE_DIR, "Slotwise.csv"))
arr = df.to_numpy()

for i in range(1, len(arr)):
    for j in range(len(arr[0])):
        if len(arr[i][j]) == 1 or len(arr[i][j]) == 5:
            for x in tt.keys():
                if x in arr[i][j]:
                    arr[i][j] = tt[x]
                    break
for i in range(1, len(arr)):
    for j in range(len(arr[0])):
        if len(arr[i][j]) == 1 or len(arr[i][j]) == 5:
            arr[i][j] = ''
arr[0][0] = ''

a = np.array(arr)
print(a)
workbook = xlsxwriter.Workbook(os.path.join(BASE_DIR, 'Timetable.xlsx'))
worksheet = workbook.add_worksheet()
r = c = 0

for i in a:
    c = 0
    for j in i:
        worksheet.write(r, c, j)
        c += 1
    r += 1

workbook.close()
