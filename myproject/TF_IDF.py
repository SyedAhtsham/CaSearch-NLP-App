

# Reading idfs
idfs = []
file = open('idf.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split(' ')
    idfs.append(float(sep[1]))

file = open('logFrequency.txt', 'r')

file2 = open('tf_idf.txt', 'w')

idfIdx = 0

if file:
    for line in file:
        data = line.strip(' \n')
        separate = data.split('\t')
        file2.write(separate[0] + '\t')
        items = separate[1].split(' ')
        for item in items:
            breakItem = item.split(':')
            docId = breakItem[0]

            logFrequency = breakItem[1]
            lf = float(logFrequency)

            tf_idf = lf * idfs[idfIdx]
            tf_idf = round(tf_idf, 3)

            file2.write(docId + ':' + str(tf_idf) + ' ')

        file2.write('\n')
        idfIdx += 1
else:
    print('File not found ...')

print('Finished ....')



