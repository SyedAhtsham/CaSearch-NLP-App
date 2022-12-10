
sumsList = []
termsList = []

file = open('tf_idf.txt', 'r')
file2 = open('top10Terms(tf_idf).txt', 'w')

if file:
    for line in file:

        score = 0
        data = line.strip(' \n')
        separate = data.split('\t')

        vocId = separate[0]

        items = separate[1].split(' ')
        for item in items:
            breakItem = item.split(':')
            docId = breakItem[0]

            tf_idf = breakItem[1]
            ti = float(tf_idf)

            score += ti

        sumsList.append(score)
        termsList.append(vocId)

else:
    print('File not found ...')

for i in range(len(sumsList)-1):
    for j in range(len(sumsList)-i-1):
        if sumsList[j] < sumsList[j+1]:
            temp = sumsList[j]
            sumsList[j] = sumsList[j+1]
            sumsList[j+1] = temp
            temp = termsList[j]
            termsList[j] = termsList[j+1]
            termsList[j+1] = temp



for i in range(10):
    file2.write(str(termsList[i]) + " " + str(sumsList[i]) + "\n")



sumsList = []
termsList = []

file3 = open('bm25.txt', 'r')
file4 = open('top10Terms(bm25).txt', 'w')

if file3:
    for line in file3:

        score = 0
        data = line.strip(' \n')
        separate = data.split('\t')

        vocId = separate[0]

        items = separate[1].split(' ')
        for item in items:
            breakItem = item.split(':')
            docId = breakItem[0]

            bm25 = breakItem[1]
            bm25_wt = float(bm25)

            score += bm25_wt

        sumsList.append(score)
        termsList.append(vocId)

else:
    print('File not found ...')

for i in range(len(sumsList)-1):
    for j in range(len(sumsList)-i-1):
        if sumsList[j] < sumsList[j+1]:
            temp = sumsList[j]
            sumsList[j] = sumsList[j+1]
            sumsList[j+1] = temp
            temp = termsList[j]
            termsList[j] = termsList[j+1]
            termsList[j+1] = temp





for i in range(10):
    file4.write(str(termsList[i]) + " " + str(sumsList[i]) + "\n")





print('Finished ....')


print('Finished ....')