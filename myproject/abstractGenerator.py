# importing required modules
import glob
import PyPDF2
import re
import pdfplumber

allFileNames = glob.glob("AllCases/*")
allFileNames.sort()


ca = open('Abstracts/c.a.txt', 'w')
cp = open('Abstracts/c.p.txt', 'w')
crl = open('Abstracts/crl.txt', 'w')
fc = open('Abstracts/f.c.txt', 'w')
mc = open('Abstracts/m.c.txt', 'w')
pc = open('Abstracts/p.c.txt', 'w')
sm = open('Abstracts/s.m.txt', 'w')

caIdx = 1
cpIdx = 1
crlIdx = 1
fcIdx = 1
mcIdx = 1
pcIdx = 1
smIdx = 1

vocabulary = set()

for name in allFileNames:
    try:
        with pdfplumber.open(name) as pdf:

            page = pdf.pages[0]
            text = page.extract_text()
            #print(name)
            matching = re.findall('C[iIvViIlL]{4}[^\)]*\)', text)
            if len(matching) > 0:
                #print(matching[0])
                ca.write(str(caIdx) + '\t' + matching[0] + '\n')




    except:
        continue

print('All abstracts are saved ...')