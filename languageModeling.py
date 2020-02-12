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
        for sentence in eachDoc:
            text = sentence.split(' ')
            text.append("<NEWLINE>")
            for i in range(len(text) - n + 1):
                g = ' '.join(text[i:i + n])
                output.append(g)
    totalCount = len(output)
    freqDistList = nltk.FreqDist(output)
    newFreqDict = calculateProb(freqDistList,totalCount)
    return newFreqDict

#calculate probability of n-gram
def calculateProb(freqDistList,totalCount):
    finalDict={}
    for items in freqDistList:
        count = freqDistList[items]
        probCount = count / totalCount
        finalDict[items] = probCount
    return finalDict

#calculate highest probability
def calHighestPossibility(userInput, ngramList):

    finalList = []
    for item in ngramList:
        splitItem = item.split(' ')
        for eachWord in splitItem:
            if userInput == eachWord:
                finalList.append((item,ngramList[item]))
    sortedList = sorted(finalList, key=lambda tup: tup[1])
    return sortedList[-1]


#create pickle
def createPickle(cwd,data,fileName):
    pickleDir = os.path.join(cwd, "_pickleFiles")
    picklePath = os.path.join(pickleDir,fileName)
    pickleFile = open(picklePath, "wb")
    pickle.dump(data, pickleFile)
    pickleFile.close()

#read pickle
def openPickleFile(cwd,fileName):
    pickleDir = os.path.join(cwd, "_pickleFiles")
    picklePath = os.path.join(pickleDir, fileName)
    pickleFile =open(picklePath, "rb")
    loadFile = pickle.load(pickleFile)
    pickleFile.close()
    return loadFile


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
# createPickle(cwd,allCorpus,"corpus.pickle")

#Deserializing corpus
tempCorpus = openPickleFile(cwd,"corpus.pickle")


#creating n grams and serializing
bigram = ngrams(tempCorpus, 2)
trigram= ngrams(tempCorpus, 3)
quadgram = ngrams(tempCorpus, 4)

createPickle(cwd,bigram,"bigram.pickle")
createPickle(cwd,bigram,"trigram.pickle")
createPickle(cwd,bigram,"quadgram.pickle")

bigramData = openPickleFile(cwd, "bigram.pickle")
trigramData = openPickleFile(cwd, "trigram.pickle")
quadgramData = openPickleFile(cwd, "quadgram.pickle")

#userInput = input("Give me a query:")
userInput = "to"
userInput = userInput.lower()
#eSwitch = True
#while eSwitch:
splitList = userInput.split(' ')
if len(splitList) == 1:
    calHighestPossibility(userInput, bigramData)
    print('bi')
elif len(splitList) == 2:
    print('tri')
elif len(splitList) == 3:
    print('quad')
else:
    print('all')

#if splitList[-1] == "<NEWLINE>":
#   eSwitch = False



# testString = "This is a sentence"
# temp = ngrams(testString,2)
# print(temp)


############# graveyard #####################

