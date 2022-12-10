
import PyPDF2
import re
import string
import glob
from string import digits
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pdfplumber

# Read Documents
documents = []
file = open('documentIndex.txt', 'r', encoding='UTF-8')
line = file.readline().strip('\n')
while line:
    documents.append(line.split(' '))
    line = file.readline().strip('\n')


# Read Vocabuary
vocabulary = []
file1 = open('sortedVocabularyWithNames.txt', 'r', encoding='UTF-8')
line = file1.readline().strip('\n')
while line:
    vocabulary.append(line.split(' '))
    line = file1.readline().strip('\n')

file2 = open('termFrequency.txt', 'w', encoding='UTF-8')

allDocsDataList = []

for docItem in documents:
    docId = docItem[0]
    docName = docItem[1]

    try:
        strData = ""
        with pdfplumber.open('AllCases/' + docName) as pdf:
            for pageNumber in range(len(pdf.pages)):
                page = pdf.pages[pageNumber]
                data = page.extract_text()

                data = data.lower()
                data = data.replace('\n', ' ')
                data = data.replace('™', '')
                data = data.replace('–', '')
                data = data.replace('•', '')

                data = data.translate(str.maketrans('', '', string.punctuation))
                data = re.sub(r'\b\w{1,3}\b', '', data)
                #remove_digits = str.maketrans('', '', digits)
                #data = data.translate(remove_digits)
                data = re.sub(r'\s+', ' ', data)

                stop_words = set(stopwords.words('english'))

                word_tokens = word_tokenize(data)

                filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

                for word in filtered_sentence:
                    strData += word + " "

        allDocsDataList.append(docId + ":" + strData)
        strData = ""

    except:
        continue


for vocabularyItem in vocabulary:
    vocId = vocabularyItem[0]
    vocName = vocabularyItem[1]

    file2.write(vocId + "\t")
    #print(vocId, end="\t")

    for docData in allDocsDataList:
        counter = 0
        separate = docData.split(':')
        docId = separate[0]
        text = separate[1]

        tokens = text.split(' ')

        for word in tokens:
            if word.find(vocName) != -1:
                counter += 1

        if counter > 0:
            file2.write(docId + ":")
            file2.write(str(counter) + " ")
        #print(counter, end=" ")

    #print()
    file2.write('\n')


print('Finished TF')