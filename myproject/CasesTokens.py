import PyPDF2
import enchant
import re
import string
import glob
from string import digits

import pdfplumber
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer

dictionary = enchant.Dict("en_US")

fileObj = open('names.txt', 'r')
names = []

for x in fileObj:
    names.append(x.strip('\n').lower())

id = 1

allFileNames = glob.glob("AllCases/*")

allFileNames.sort()

for name in allFileNames:
    try:

        pdfFileObj = open(name, 'rb')
        name2 = name.split('\\')
        file = open('File cases tokens\\' + name2[1] + '.txt', 'w')
        vocabulary = []

        with pdfplumber.open(name) as pdf:
            for pageNumber in range(len(pdf.pages)):
                page = pdf.pages[pageNumber]

                data = page.extract_text()

                data = data.lower()
                data = data.replace('\n', ' ')
                data = data.replace('™', '')
                data = data.replace('–', '')

                data = data.translate(str.maketrans('', '', string.punctuation))
                data = re.sub(r'\b\w{1,3}\b', '', data)
                data = re.sub(r'\s+', ' ', data)

                stop_words = set(stopwords.words('english'))

                word_tokens = word_tokenize(data)

                filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

                lemmatizer = WordNetLemmatizer()
                ps = PorterStemmer()

                for item in filtered_sentence:
                    item = item.replace('‚', '')
                    item = lemmatizer.lemmatize(item)
                    item = ps.stem(item)
                    if item not in vocabulary:
                        if (item in names):
                            file.write(item + '\n')
                            vocabulary.append(item)
                        elif item.isdigit():
                            year = int(item)
                            if (year >= 1947 and year <= 2021):
                                file.write(item + '\n')
                                vocabulary.append(item)
                        elif len(item) > 3 and dictionary.check(item):
                            file.write(item + '\n')
                            vocabulary.append(item)



    except:
        continue
