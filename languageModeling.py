#Oliver Chen
#Chase Moore
#Jared Mello

import os
import re
import string
import nltk
from nltk.tokenize import sent_tokenize
import pickle


#Lower case everything, remove punctuation, sentence segmentation
def preprocessing(corpus):
    sentencesList = sent_tokenize(corpus)
    cleanCorpus = []
    for eachSent in sentencesList:
        textNoP = eachSent.translate(str.maketrans("", "", string.punctuation))
        textNoN = re.sub(r'(\n+)',' ',textNoP)
        lowerText = textNoN.lower()
        cleanCorpus.append(lowerText)
    return cleanCorpus


#get the raw text from the file
def getText(filename):
    file = open(filename, 'rt')
    text = file.read()
    file.close()
    return text

#ngrams function
def ngrams(input, n):
    input = input.split(' ')
    output = {}
    for i in range(len(input) - n + 1):
        g = ' '.join(input[i:i+n])
        output.setdefault(g, 0)
        output[g] += 1
    return output

#writes bigram, trigram and quadgram files to the directory
def writeNGrams(corpus):
    i = 2
    #gets ngrams for austen-emma
    while i < 5:
        file = open(str(i) + "gram.txt", "wt")
        temp = str(ngrams(str(corpus[0]), i))
        file.write(temp)
        file.close()
        i += 1


#====================================================================================================
#Main
cwd = os.getcwd()
inputDir = os.path.join(cwd,"_input")
pickleDir = os.path.join(cwd,"_pickleFiles")
#Load all corpus
listOfInputName = os.listdir(inputDir)
allCorpus = []

#append the normalized sentences to a list
for eachFile in listOfInputName:
    currentInputPath = os.path.join(inputDir,eachFile)
    currentInputText = getText(currentInputPath)
    currentSentences = preprocessing(currentInputText)
    allCorpus.append(currentSentences)


#Serializing corpus
corpusPicklePath = os.path.join(pickleDir, "corpus.pickle")
corpusPickleFile = open(corpusPicklePath,"wb")
pickle.dump(allCorpus, corpusPickleFile)
corpusPickleFile.close()

#Deserializing corpus
readTemp = open(corpusPicklePath, "rb")
tempCorpus = pickle.load(readTemp)
readTemp.close()


print(writeNGrams(tempCorpus))

# testString = "this is a sentence"
# temp = ngrams(testString,2)
# print(temp)


############# graveyard #####################


# def g():
#   global big
#   big = file('big.txt').read()
#   N = len(big)
#   s = set()
#   for i in xrange(6, N):
#     c = big[i]
#     if ord(c) > 127 and c not in s:
#         print i, c, ord(c), big[max(0, i-10):min(N, i+10)]
#         s.add(c)
#   print s
#   print [ord(c) for c in s]
