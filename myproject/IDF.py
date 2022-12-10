import math

N = 1000

file2 = open('idf.txt', 'w')

file = open('documentFrequency.txt', 'r')
if file:
    for line in file:
        data = line.strip('\n')
        sep = data.split(' ')
        vocId = sep[0]
        df = int(sep[1])

        idf = 0
        if df > 0:
            value = N/df
            idf = math.log10(value)
            idf = round(idf, 3)


        file2.write(vocId + ' ' + str(idf) + '\n')
