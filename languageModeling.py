#Huan-Yun Chen (Oliver)
#Chase Moore
#Jared Mello

import os
import sys
import re
import string
import pickle
from random import randint
import nltk
from nltk.tokenize import sent_tokenize

#lower case everything, remove punctuation, sentence segmentation
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

#process user input query
def process(userInput,bigramData,trigramData,quadgramData):
    userInput = userInput.lower()
    userInput = userInput.strip()
    eSwitch = True
    finalSentence = userInput
    print("------------------------------------------")
    print("query:" + str(userInput))
    print("Sentence Progression: ")
    while eSwitch:
        splitList = userInput.split(' ')
        #print(splitList)
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
            words,probValue = calHighestPossibility(userInput, trigramData)
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
            words,probValue = calHighestPossibility(userInput, quadgramData)
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
        if len(finalSentence) > 500:
            break
        if splitList[0] == '':
            break
        print(finalSentence)
    return finalSentence
    

#====================================================================================================
#Main
cwd = os.getcwd()
inputDir = os.path.join(cwd,"_input")
pickleDir = os.path.join(cwd,"_pickleFiles")
testDir = os.path.join(cwd,"_test")
userArgv = sys.argv[1]

# -c or -create: create pickle files for corpus and n-gram
if userArgv == "-c" or userArgv == "-create":
    print("Loading Corpus ...")
    #Load all corpus files
    listOfInputName = os.listdir(inputDir)
    allCorpus = []
    print("Normalizing Corpus ...")
    #append the normalized sentences to a list
    for eachFile in listOfInputName:
        currentInputPath = os.path.join(inputDir,eachFile)
        currentInputText = getText(currentInputPath)
        currentSentences = preprocessing(currentInputText)
        allCorpus.append(currentSentences)
    print("Creating Corpus Pickle ...")
    #Create corpus pickle
    createPickle(cwd,allCorpus,"corpus.pickle")
    print("Creating n-gram ...")
    #creating n grams and store in pickle
    bigram = ngrams(allCorpus, 2)
    trigram= ngrams(allCorpus, 3)
    quadgram = ngrams(allCorpus, 4)
    print("Creating n-gram Pickle ...")
    createPickle(cwd,bigram,"bigram.pickle")
    createPickle(cwd,trigram,"trigram.pickle")
    createPickle(cwd,quadgram,"quadgram.pickle")

#-q or -query: allow user to query with system provide a word or a sentence to predict possible sentence after that
elif userArgv == "-q" or userArgv == "-query":
    #load corpus pickle
    tempCorpus = openPickleFile(cwd,"corpus.pickle")
    #load ngram pickle
    bigramData = openPickleFile(cwd, "bigram.pickle")
    trigramData = openPickleFile(cwd, "trigram.pickle")
    quadgramData = openPickleFile(cwd, "quadgram.pickle")

    userInput = input("Give me a query:")
    final = process(userInput,bigramData,trigramData,quadgramData)
    print('\n Final Sentence: '+ str(final))

#testing argument, given a file and extract part of the sentence feed it into the system, then compare the result with the original sentence
elif userArgv == "-t" or userArgv == "-test":
    testNumSentence = 100
    #Load all test files
    print("Normalizing test file ...")
    #append the normalized sentences to a list
    currentInputPath = os.path.join(testDir,"test.txt")
    currentInputText = getText(currentInputPath)
    currentSentences = preprocessing(currentInputText)
    allTest = currentSentences[:testNumSentence]

    #load ngram pickle
    bigramData = openPickleFile(cwd, "bigram.pickle")
    trigramData = openPickleFile(cwd, "trigram.pickle")
    quadgramData = openPickleFile(cwd, "quadgram.pickle")

    testList = []
    for eachTest in allTest:
        splitTestList = eachTest.split(' ')
        start = randint(0,len(splitTestList))
        end = randint(start,len(splitTestList))
        sentence = splitTestList[start:end]
        testString = ""
        for each in sentence:
            testString = testString + " " + each
        testString = testString.strip()
        if not testString == "":
            testList.append(testString)
    
    testFilePath = os.path.join(cwd,'testOutput.txt')
    testFile = open(testFilePath,"w")
    for eachTest in testList:
        final = process(eachTest,bigramData,trigramData,quadgramData)
        testFile.write(str(final)+"\n")
    testFile.close()

else:
    print("The command argument is not valid please read the documentation")


############# END #####################

