

i = 1
while i <= 53:
    filename = 'f.c_' + str(i) + '.pdf.txt'
    try:
        file = open('File cases tokens\\' + filename, 'a')
        file.write('family')
        file.write('\n')
        file.write('case')
    except:
        print(filename)

    i += 1


i = 1
while i <= 80:
    filename = 'h.r_' + str(i) + '.pdf.txt'
    try:
        file = open('File cases tokens\\' + filename, 'a')
        file.write('rape')
        file.write('\n')
        file.write('case')
    except:
        print(filename)

    i += 1

