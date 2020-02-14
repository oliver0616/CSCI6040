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
        sameWords = True
        if userInput in item:
            itemList = item.split(' ')
            userInputList = userInput.split(' ')
            ngramPointer = 0
            for eachUserWord in userInputList:
                if eachUserWord == itemList[ngramPointer]:
                    ngramPointer+=1
                else:
                    sameWords = False
                    break
            if sameWords:
                finalList.append((item,ngramList[item]))
    sortedList = sorted(finalList, key=lambda tup: tup[1])
    if len(sortedList) == 1:
        return sortedList[0]
    elif not len(sortedList) == 0: 
        return sortedList[-1]
    else:
        return ("<NONE>",0)


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
#createPickle(cwd,allCorpus,"corpus.pickle")

#Deserializing corpus
tempCorpus = openPickleFile(cwd,"corpus.pickle")


#creating n grams and serializing
bigram = ngrams(tempCorpus, 2)
trigram= ngrams(tempCorpus, 3)
quadgram = ngrams(tempCorpus, 4)

#createPickle(cwd,bigram,"bigram.pickle")
#createPickle(cwd,bigram,"trigram.pickle")
#createPickle(cwd,bigram,"quadgram.pickle")

bigramData = openPickleFile(cwd, "bigram.pickle")
trigramData = openPickleFile(cwd, "trigram.pickle")
quadgramData = openPickleFile(cwd, "quadgram.pickle")

#userInput = input("Give me a query:")
userInput = "this is the last one"
userInput = userInput.lower()
eSwitch = True
finalSentence = userInput

while eSwitch:
    splitList = userInput.split(' ')
    if len(splitList) == 1:
        words,probValue = calHighestPossibility(userInput, bigramData)
        if words == "<NONE>":
            break
        wordsList = words.split(' ')
        userInput = words
        finalSentence = finalSentence +" "+ wordsList[-1]
        if wordsList[-1] == "<NEWLINE>":
            break
    elif len(splitList) == 2:
        words,probValue = calHighestPossibility(userInput, trigram)
        if words == "<NONE>":
            userInputList = userInput.split(' ')
            userInput = ""
            for each in userInputList[1:]:
                userInput = userInput+" "+each
            userInput = userInput.strip()
            continue
        wordsList = words.split(' ')
        userInput = words
        finalSentence = finalSentence +" "+wordsList[-1]
        if wordsList[-1] == "<NEWLINE>":
            break
    elif len(splitList) == 3:
        words,probValue = calHighestPossibility(userInput, quadgram)
        if words == "<NONE>":
            userInputList = userInput.split(' ')
            userInput = ""
            for each in userInputList[1:]:
                userInput = userInput+" "+each
            userInput = userInput.strip()
            continue
        wordsList = words.split(' ')
        userInput = words
        finalSentence = finalSentence +" "+ wordsList[-1]
        if wordsList[-1] == "<NEWLINE>":
            break
    else:
        userInputList = userInput.split(' ')
        userInput = ""
        for each in userInputList[1:]:
            userInput = userInput+" "+each
        userInput = userInput.strip()

    print(finalSentence)

        

#if splitList[-1] == "<NEWLINE>":
#   eSwitch = False



# testString = "This is a sentence"
# temp = ngrams(testString,2)
# print(temp)


############# graveyard #####################

