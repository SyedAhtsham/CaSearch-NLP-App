import os

murderIdx = 0
suoMotoIdx = 0
civilAppealIdx = 0
civilPetition = 0
humanIdx = 0
propertyIdx = 0
familyIdx = 0
criminalIdx = 0

import glob

allFileNames = glob.glob("AllCases/*")

print(allFileNames)

justNames = []

for name in allFileNames:
    justNames.append(name.split('\\')[1])

justNames.sort()

for name2 in justNames:
    print(name2)

file = open('documentIndex.txt', 'w')
for i in range(0, len(justNames)):
    file.write(str(i + 1) + ' ' + justNames[i] + '\n')
file.close()