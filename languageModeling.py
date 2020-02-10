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
    output = []
    for eachDoc in input:
        eachDocList=[]
        for sentence in eachDoc:
            text = sentence.split(' ')
            for i in range(len(text) - n + 1):
                g = ' '.join(text[i:i + n])
                eachDocList.append(g)
        output.append(eachDocList)
    # input = input.split(' ')
    # output = {}
    # for i in range(len(input) - n + 1):
    #     g = ' '.join(input[i:i+n])
    #     output.setdefault(g, 0)
    #     output[g] += 1
    return output

#create pickle
def createPickel(data,fileName):
    pickleDir = os.path.join(cwd, "_pickleFiles")

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

#creating n grams
uniPicklePath = os.path.join(pickleDir, "unigram.pickle")
biPicklePath = os.path.join(pickleDir, "bigram.pickle")
triPicklePath = os.path.join(pickleDir, "trigram.pickle")
quadPicklePath = os.path.join(pickleDir, "quadgram.pickle")
uniPickleFile = open(uniPicklePath,"wb")
biPickleFile = open(biPicklePath,"wb")
triPickleFile = open(triPicklePath,"wb")
quadPickleFile = open(quadPicklePath,"wb")
unigram = ngrams(tempCorpus,1)
bigram = ngrams(tempCorpus, 2)
trigram= ngrams(tempCorpus, 3)
quadgram = ngrams(tempCorpus, 4)
pickle.dump(unigram, uniPickleFile)
pickle.dump(bigram, biPickleFile)
pickle.dump(trigram, triPickleFile)
pickle.dump(quadgram, quadPickleFile)

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
