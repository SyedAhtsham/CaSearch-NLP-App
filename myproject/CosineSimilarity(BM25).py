import math



docIndexes = []
bm25Values = []
vocabulary = dict()
queries = []
idfs = dict()
docFrequencies = dict()

k = 5
N = 1000




def getTermFrequency(vocId, docId):
    file = open('termFrequency.txt', 'r')
    for line in file:
        data = line.strip('\n')
        sep = data.split('\t')
        vId = sep[0]
        if vId == vocId:
            values = sep[1].split(' ')
            for item in values:
                sep2 = item.split(':')
                if docId == sep2[0]:
                    return float(sep2[1])
    return 0

def L2NormOfVector(vector):
    result = 0
    total = 0
    for value in vector:
        total = total + (value * value)
    result = math.sqrt(total)
    return result

def countWordsInText(word, text):
    tokens = text.split(' ')
    count = 0
    for token in tokens:
        if token == word:
            count += 1
    return count

def getVocabularyId(voc):
    try:
        return vocabulary[voc]
    except:
        return '0'


def getBm25ForDoc(vocId, docId):
    for item in bm25Values:
        if item[0] == vocId:
            sep = item[1].split(' ')
            for item2 in sep:
                breakItem = item2.split(':')
                if breakItem[0] == docId:
                    return float(breakItem[1])
    return 0.0

def getNormalizedVector(vector):
    l2Norm = L2NormOfVector(vector)
    normalized = []
    if l2Norm > 0:
        for value in vector:
            val = float(value / l2Norm)
            normalized.append(val)
        return normalized
    return vector

def getBm25ForQuery(vocId, docId, query):
    cw_query = countWordsInText(word, query)
    bm25ForDoc = getBm25ForDoc(vocId, docId)
    bm25 = cw_query * bm25ForDoc
    return bm25


def computeDotProduct(vector1, vector2):
    result = 0
    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]
    return result

# Read document frequencies
file = open('documentFrequency.txt', 'r')
if file:
    for line in file:
        data = line.strip('\n')
        sep = data.split(' ')
        vocId = sep[0]
        df = int(sep[1])
        docFrequencies[vocId] = df

# Read document indexes
file = open('documentIndex.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split(' ')
    docIndexes.append(sep)
file.close()

# Read bm25
file = open('bm25.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split('\t')
    bm25Values.append(sep)
file.close()

# Read vocabulary
file = open('sortedVocabularyWithNames.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split(' ')
    vocabulary[sep[1]] = sep[0]
file.close()
# Read queries from file
file = open('queries(bm25).txt', 'r')
for line in file:
    data = line.strip('\n')
    queries.append(data)
file.close()

# Read idfs
file = open('idf.txt', 'r')
for line in file:
    data = line.strip('\n')
    sep = data.split(' ')
    idfs[sep[0]] = float(sep[1])

file.close()
queryIdx = 1

file2 = open('cosineScores(bm25).txt', 'w')


for query in queries:

    docNames = []
    scores = []

    query.lower()
    queryTokens = query.split(' ')

    file2.write(query + '\n')
    file2.write('Weighting Scheme: BM25' + '\n')

    # Read tokens for each document
    for item in docIndexes:

        wordsSet = set()
        docScoreVector = []



        docId = item[0]
        docName = 'File cases tokens\\' + item[1] + '.txt'
        file = open(docName, 'r')
        for line in file:
            token = line.strip('\n')
            if token in queryTokens:
                wordsSet.add(token)

        # Document Part
        for word in wordsSet:
            bm25_val = 0
            vocId = getVocabularyId(word)
            if vocId != '0':
                bm25_val = getBm25ForQuery(vocId, docId, query)
            docScoreVector.append(float(bm25_val))

        bm25Score = 0
        for item in docScoreVector:
            bm25Score += item

        if bm25Score > 0:
            scores.append(round(bm25Score, 3))
            docNames.append(docName)

    if len(scores) > 0:
        for i in range(len(scores)-1):
            for j in range(len(scores)-i-1):
                if scores[j] < scores[j+1]:
                    temp = scores[j]
                    scores[j] = scores[j+1]
                    scores[j+1] = temp
                    temp = docNames[j]
                    docNames[j] = docNames[j+1]
                    docNames[j+1] = temp

        i = 0
        while i < len(scores) and i < 10:
            file2.write(docNames[i] + ' ' + str(scores[i]) + '\n')
            i += 1

    else:
        file2.write('No Documents Found\n')

    file2.write('\n')

file2.close()
print('\n > All data is saved into text file ...')