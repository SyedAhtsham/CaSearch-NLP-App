import math

docFrequencies = []

file = open('documentFrequency.txt', 'r')
if file:
    for line in file:
        data = line.strip('\n')
        sep = data.split(' ')
        vocId = sep[0]
        df = int(sep[1])
        docFrequencies.append(df)

file2 = open('termFrequency.txt', 'r')
file3 = open('bm25.txt', 'w')

dfIdx = 0
k = 5
N = 1000

if file2:
    for line in file2:
        data = line.strip(' \n')
        separate = data.split('\t')
        file3.write(separate[0] + '\t')
        items = separate[1].split(' ')
        for item in items:
            breakItem = item.split(':')
            docId = breakItem[0]

            tFrequency = breakItem[1]
            tf = int(tFrequency)

            bm25 = 0
            if docFrequencies[dfIdx] > 0:
                bm25 = ((k+1) * tf) / (tf + k)
                value = (N+1) / docFrequencies[dfIdx]
                bm25 = bm25 * math.log10(value)
                bm25 = round(bm25, 3)

            file3.write(docId + ':' + str(bm25) + ' ')

        file3.write('\n')
        dfIdx += 1
else:
    print('File not found ...')

print('Finished ....')

k = 5