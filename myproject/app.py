import re
import string
import textwrap

import pdfplumber
from flask import Flask, render_template, url_for, request, redirect

import matplotlib.pyplot as plt
from nltk import word_tokenize, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from wordcloud import WordCloud

import math


docIndexes = []
bm25Values = []
vocabulary = dict()
idfs = dict()
docFrequencies = dict()
abstractsDictionary = dict()
gAbstract = 'CIVIL APPEAL NO.1474. OF 2015 (Against the judgment dated _16.12.2014 passed by the Peshawar High Court, Peshawar in Writ Petition No.162 of 2014).'
k = 5
N = 1000


def extractAbstracts():
    file = open('abstracts.txt', 'r')
    for line in file:
        line = line.strip('\n')
        data = line.split(':')
        abstractsDictionary[data[0]] = data[1]

def makeWordCloud(wordsList):
    if len(wordsList) > 0:
        # convert list to string and generate
        unique_string = (" ").join(wordsList)
        wordcloud = WordCloud(width=400, height=350).generate(unique_string)
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig("Static\\cloud" + ".png", bbox_inches='tight')
        # plt.show()
        plt.close()


def getTokensForDocument(docName):
    words = []
    data = docName.split('/')
    file = open('File cases tokens\\' + data[1] + '.txt')
    if file:
        for line in file:
            words.append(line.strip('\n'))
        return words

def getAbstract(filename):
    data = filename.split('_')
    return 'Here .... ' + abstractsDictionary[data[0]]

def extractAbstractOfDocument(docName):
    abstract = ""
    try:
        with pdfplumber.open('AllCases\\' + docName) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            # onAppeal = re.findall('\(On\s[AaPpPpEeAaLl]{6}[^\)]*\)', text)
            # if len(onAppeal) > 0:
            #     return onAppeal[0]
            ca = re.findall('C[iIvViIlL]{4}[^\)]*\)', text)
            if len(ca) > 0:
                return ca[0]
            cp = re.findall('C[IiVviIlL]{4}[^\)]*\)', text)
            if len(cp) > 0:
                return cp[0]
            crl = re.findall('C[RrIiMmIiNnAaLl]{7}[^\)]*\)', text)
            if len(crl) > 0:
                return crl[0]
            crl = re.findall('C[RrIiMmIiNnAaLl]{7}[^\)]*\)', text)
            if len(crl) > 0:
                return crl[0]
            hr = re.findall('H[UuMmAaNn]{4}[^\)]*\)', text)
            if len(hr) > 0:
                return hr[0]
            hr = re.findall('H[.RC]{4}[^\)]*\)', text)
            if len(hr) > 0:
                return hr[0]
            smc = re.findall('S[uUoO]{2}[^\)]*\)', text)
            if len(smc) > 0:
                return smc[0]
            smc = re.findall('S[\.M\.C]{4}[^\)]*\)', text)
            if len(smc) > 0:
                return smc[0]
    except:
        print('here')
        return abstract
    return abstract


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


def getBm25ForQuery(word, vocId, docId, query):
    cw_query = countWordsInText(word, query)
    bm25ForDoc = getBm25ForDoc(vocId, docId)
    bm25 = cw_query * bm25ForDoc
    return bm25


def computeDotProduct(vector1, vector2):
    result = 0
    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]
    return result


def runQuery(queryText):
    relevantdocs = []
    relevantAbstracts = []

    queries = [queryText]
    extractAbstracts()

    print(abstractsDictionary)

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

        query = query.lower()
        query = query.replace('\n', ' ')
        query = query.replace('™', '')
        query = query.replace('–', '')
        query = query.replace('•', '')

        query = query.translate(str.maketrans('', '', string.punctuation))
        query = re.sub(r'\b\w{1,3}\b', '', query)
        query = re.sub(r'\s+', ' ', query)
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(query)
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        queryTokens = []
        ps = PorterStemmer()
        wordnet_lemmatizer = WordNetLemmatizer()
        for item in filtered_sentence:
            item2 = ps.stem(item)
            queryTokens.append(item2)

        # Read tokens for each document
        for item in docIndexes:

            wordsSet = set()
            docScoreVector = []

            docId = item[0]
            docName = 'File cases tokens\\' + item[1] + '.txt'
            file = open(docName, 'r', encoding="ISO-8859-1")

            for line in file:
                token = line.strip('\n')
                if token in queryTokens:
                    wordsSet.add(token)

            # Document Part
            for word in wordsSet:
                bm25_val = 0
                vocId = getVocabularyId(word)
                if vocId != '0':
                    bm25_val = getBm25ForQuery(word, vocId, docId, query)
                docScoreVector.append(float(bm25_val))

            bm25Score = 0
            for item in docScoreVector:
                bm25Score += item

            if bm25Score > 0:
                scores.append(round(bm25Score, 3))
                docNames.append(docName)

        if len(scores) > 0:
            for i in range(len(scores) - 1):
                for j in range(len(scores) - i - 1):
                    if scores[j] < scores[j + 1]:
                        temp = scores[j]
                        scores[j] = scores[j + 1]
                        scores[j + 1] = temp
                        temp = docNames[j]
                        docNames[j] = docNames[j + 1]
                        docNames[j + 1] = temp

            i = 0
            abstract = ''
            while i < len(scores) and i < 100:
                separate = docNames[i].split('.txt')
                onlyPdf = separate[0].split('File cases tokens\\')

                if str('AllCases/' + onlyPdf[1]) not in relevantdocs:
                    relevantdocs.append('AllCases/' + onlyPdf[1])
                    abstract = extractAbstractOfDocument(onlyPdf[1])

                if len(abstract) > 170:
                    abstract = textwrap.shorten(abstract, width=170, placeholder="...")
                if abstract == '':
                    abstract = getAbstract(onlyPdf[1])
                else:
                    relevantAbstracts.append(abstract)
                file2.write(docNames[i] + ' ' + str(scores[i]) + '\n')
                i += 1

        else:
            file2.write('No Documents Found\n')

        file2.write('\n')

    file2.close()
    print('\n > All data is saved into text file ...')
    return relevantdocs, relevantAbstracts


app = Flask(__name__)
page1docs = []
page1Abs = []
page2docs = []
page2Abs = []
page3docs = []
page3Abs = []
page4docs = []
page4Abs = []
page5docs = []
page5Abs = []
page6docs = []
page6Abs = []
page7docs = []
page7Abs = []
page8docs = []
page8Abs = []
page9docs = []
page9Abs = []
page10docs = []
page10Abs = []
relevantDocs = []
relevantAbstracts = []
noOfPages = 0
isYes = True
prevQuery = ""


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        global noOfPages, relevantAbstracts, relevantDocs, isYes, prevQuery

        pageNo = request.form['pageNo']

        query = request.form['query']
        if query != prevQuery:
            isYes = True
            page1docs.clear()
            page1Abs.clear()
            page2docs.clear()
            page2Abs.clear()
            page3docs.clear()
            page3Abs.clear()
            page4docs.clear()
            page4Abs.clear()
            page5docs.clear()
            page5Abs.clear()
            page6docs.clear()
            page6Abs.clear()
            page7docs.clear()
            page7Abs.clear()
            page8docs.clear()
            page8Abs.clear()
            page9docs.clear()
            page9Abs.clear()
            page10docs.clear()
            page10Abs.clear()
            relevantDocs.clear()
            relevantAbstracts.clear()

        print(noOfPages)
        print(isYes)
        print(pageNo)

        if isYes:
            relevantDocs, relevantAbstracts = runQuery(query)

            k = 0
            for doc in relevantDocs:
                if k < 10:
                    page1docs.append(doc)
                    page1Abs.append(relevantAbstracts[k])
                elif k < 20:
                    page2docs.append(doc)
                    page2Abs.append(relevantAbstracts[k])
                elif k < 30:
                    page3docs.append(doc)
                    page3Abs.append(relevantAbstracts[k])
                elif k < 40:
                    page4docs.append(doc)
                    page4Abs.append(relevantAbstracts[k])
                elif k < 50:
                    page5docs.append(doc)
                    page5Abs.append(relevantAbstracts[k])
                elif k < 60:
                    page6docs.append(doc)
                    page6Abs.append(relevantAbstracts[k])
                elif k < 70:
                    page7docs.append(doc)
                    page7Abs.append(relevantAbstracts[k])
                elif k < 80:
                    page8docs.append(doc)
                    page8Abs.append(relevantAbstracts[k])
                elif k < 90:
                    page9docs.append(doc)
                    try:
                        page9Abs.append(relevantAbstracts[k])
                    except:
                        page9Abs.append(gAbstract)
                elif k < 100:
                    page10docs.append(doc)
                    try:
                        page10Abs.append(relevantAbstracts[k])
                    except:
                        page10Abs.append(gAbstract)

                k += 1
            prevQuery = query
            noOfPages = math.ceil(len(relevantDocs) / 10)
        isYes = False

        if pageNo == '1':
            wordsListForWordCloud = []
            for doc in page2docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page2docs), queryText=query,
                                   docs=page2docs, abstracts=page2Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '2':
            wordsListForWordCloud = []
            for doc in page3docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page3docs), queryText=query,
                                   docs=page3docs, abstracts=page3Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '3':
            wordsListForWordCloud = []
            for doc in page4docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page4docs), queryText=query,
                                   docs=page4docs, abstracts=page4Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '4':
            wordsListForWordCloud = []
            for doc in page5docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page5docs), queryText=query,
                                   docs=page5docs, abstracts=page5Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '5':
            wordsListForWordCloud = []
            for doc in page6docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page6docs), queryText=query,
                                   docs=page6docs, abstracts=page6Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '6':
            wordsListForWordCloud = []
            for doc in page7docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page7docs), queryText=query,
                                   docs=page7docs, abstracts=page7Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '7':
            wordsListForWordCloud = []
            for doc in page8docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page8docs), queryText=query,
                                   docs=page8docs, abstracts=page8Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '8':
            wordsListForWordCloud = []
            for doc in page9docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page9docs), queryText=query,
                                   docs=page9docs, abstracts=page9Abs, pageNo=int(pageNo) + 1)
        elif pageNo == '9':
            wordsListForWordCloud = []
            for doc in page10docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page10docs), queryText=query,
                                   docs=page10docs, abstracts=page10Abs, pageNo=int(pageNo) + 1)
        else:
            wordsListForWordCloud = []
            for doc in page1docs:
                wordsInDoc = getTokensForDocument(doc)
                for word in wordsInDoc:
                    wordsListForWordCloud.append(word)
            makeWordCloud(wordsListForWordCloud)
            return render_template('fetch_docs.html', noOfPages=noOfPages, len=len(page1docs), queryText=query,
                                   docs=page1docs, abstracts=page1Abs, pageNo=int(pageNo) + 1)

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)