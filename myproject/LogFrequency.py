import math

file = open('termFrequency.txt', 'r')

file2 = open('logFrequency.txt', 'w')

if file:
    for line in file:
        data = line.strip(' \n')
        separate = data.split('\t')
        file2.write(separate[0] + '\t')
        items = separate[1].split(' ')
        for item in items:
            breakItem = item.split(':')
            docId = breakItem[0]

            tFrequency = breakItem[1]
            tf = int(tFrequency)
            logFrequency = 0
            if tf > 0:
                logFrequency = 1 + math.log10(tf)
                logFrequency = round(logFrequency, 3)
            file2.write(docId + ':' + str(logFrequency) + ' ')

        file2.write('\n')
else:
    print('File not found ...')

print('Finished ....')