


file = open('termFrequency.txt', 'r')

file2 = open('documentFrequency.txt', 'w')


if file:
    for line in file:
        line = line.strip('\n')
        sep = line.split('\t')

        vocId = sep[0]
        file2.write(vocId + ' ')

        frequencies = sep[1].split(' ')
        counter = 0

        for i in range(len(frequencies)-1):
            if frequencies[i][-1] != '0':
                counter += 1

        file2.write(str(counter) + '\n')


file2.close()
print('Done')