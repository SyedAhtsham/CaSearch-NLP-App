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


file = open('vocabulary.txt', 'w', encoding='UTF-8')

id = 1

allFileNames = glob.glob("AllCases/*")
allFileNames.sort()


vocabulary = set()

for name in allFileNames:
    try:
        with pdfplumber.open(name) as pdf:
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
                remove_digits = str.maketrans('', '', digits)
                data = data.translate(remove_digits)
                data = re.sub(r'\s+', ' ', data)

                stop_words = set(stopwords.words('english'))

                word_tokens = word_tokenize(data)

                filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

                ps = PorterStemmer()
                wordnet_lemmatizer = WordNetLemmatizer()

                for item in filtered_sentence:
                    item2 = ps.stem(item)

                    if len(item2) > 3:
                        file.write(item2 + '\n')

    except:
        continue

file.close()
print('Vocabulary is written into vocabulary.txt file ...')

"""
Helping Code:


from nltk.stem import PorterStemmer
import enchant


dictionary = enchant.Dict("en_US")

data = set()
ps = PorterStemmer()

file = open('vocabulary.txt', 'r', encoding='UTF-8')
line = file.readline().strip('\n')
while line:
    sep = line.split(' ')
    stem = ps.stem(sep[1])
    data.add(stem)
    line = file.readline().strip('\n')

print(len(data))

data2 = list(data)
data2.sort()

id = 1
for item in data2:
    if dictionary.check(item):
        print(str(id), item)
        id += 1

"""