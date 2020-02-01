#Oliver Chen
#Chase Moore
#Jared Mello

import re
import string
import pickle
from bs4 import BeautifulSoup

def preprocessing(fName, n):
    text = getText('austen-emma.txt')
    text = removePunctuation(text)
    text = tagSentenceAndNormalize(text)
    #segmentSentence(text)
    print(text)


    # normalizedText = normalize(text)


   # return ngrams(text, n)

def segmentSentence(text):
    soup = BeautifulSoup(text)
    for sentences in soup.find_all('s'):
        print(sentences)



def removePunctuation(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def tagSentenceAndNormalize(text):
        text = re.sub('  ', '</s><s>', text)
        text = text.lower()
        return text


def getText(filename):
    file = open(filename, 'rt')
    text = file.read()
    file.close()
    return text

def ngrams(input, n):
    input = input.split(' ')
    output = {}
    for i in range(len(input) - n + 1):
        g = ' '.join(input[i:i+n])
        output.setdefault(g, 0)
        output[g] += 1
    return output

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

preprocessing('big.txt', 2)
