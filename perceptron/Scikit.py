#import numpy as np
import os
import re
import math
from pandas import  DataFrame
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


wordsList = {}

spamwordsList=[]
hamwordList=[]
fileTokenMap={}
weightsMap ={}
testfileTokenMap={}
testweightsMap ={}

fileData = []
tokenCountMap = {}
weightVector={}
eta = .01
lamda = 3.5


global hamcorrect
global hamwrong
global spamcorrect
global spamwrong

def getAllWords(datapath,stopwordsPath=None):
    pathham = datapath +'/ham'
    pathspam = datapath +'/spam'
    dirham = os.listdir(pathham)
    dirspam = os.listdir(pathspam)
    sectionspam =""
    sectionham =""
    spamData = []
    stopWords = []
    if stopwordsPath is not None:
        f = open(stopwordsPath, 'r')
        regex = re.compile('\\W*')
        stopWords = regex.split(f.read())
        f.close()
    for file in dirham:
        hamfilePath = pathham +'/' + file
        f=open(hamfilePath,'r')
        sectionread = f.read()
        sectionham += sectionread
        regex = re.compile('\\W*')
        hamtokens = regex.split(sectionread)
        hamtokensList = [singleToken.lower() for singleToken in hamtokens if (len(singleToken) >1 and singleToken not in stopWords)]
        store = {}
        error = 0
        for token in hamtokensList:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0

            if not weightVector.has_key(token):
                weightVector[token] = 0

        fileData.append({'fileName':file,'text':sectionread,'fileTokens':store,'class':1})
        f.close()

    for file in dirspam:
        spamfilePath = pathspam + '/' + file
        f = open(spamfilePath, 'r')
        se0ctionread = f.read()
        sectionspam+=sectionread
        regex =  re.compile('\\W*')
        spamtokens= regex.split(sectionread)
        spamtokensList = [singleToken.lower() for singleToken in spamtokens if (len(singleToken) >1 and singleToken not in stopWords)]
        store = {}
        for token in spamtokensList:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0

            if not weightVector.has_key(token):
                weightVector[token] = 0

        fileData.append({'fileName':file,'text':sectionread,'fileTokens':store,'classVal':0})

        f.close()
   # perceptronTrain()
    build_data_frame('','')

def build_data_frame(path, classification):
    rows = []
    index = []
    for data in fileData:
        rows.append({'text': data.text, 'class': data.classVal})
        index.append(data.fileName)

    data_frame = DataFrame(rows, index=index)
    return data_frame

data = DataFrame({'text': [], 'class': []})
data = data.append(build_data_frame('',''))
data = data.reindex(numpy.random.permutation(data.index))

count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(data['text'].values)

classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)


if __name__ == "__main__":
    getAllWords("assignment3/hw2_train/train")

