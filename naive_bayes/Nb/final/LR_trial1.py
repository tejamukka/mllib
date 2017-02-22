import numpy as np
import os
import re
import math


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
eta = 0.01
lamda = 0.35

def calcSigmoid(z):
    denom = 1+np.exp(z)
    return 1-(1/denom)

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
        sectionread = f.read()
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

        fileData.append({'fileName':file,'text':sectionread,'fileTokens':store,'class':0})
        f.close()

def gradientDescent():
    keys = weightVector.keys()
    for i in range(1,200):
        updateError()
        updateWeights()

def updateError():
    for eachFile in fileData:
        keys = eachFile["fileTokens"]
        sum = 0
        for token in keys:
            sum += keys[token]*weightVector[token]
        eachFile["error"] = calcSigmoid(sum)

def updateWeights():
    keys = weightVector.keys()
    for token in keys:
        sum = 0
        for eachFile in fileData:
            tokens = eachFile["fileTokens"]
            trueValue = eachFile["class"]
            if tokens.has_key(token):
               sum +=tokens[token]*(trueValue-eachFile["error"])

        weightVector[token]+= ((sum*eta)-(eta*lamda *weightVector[token]))

def test(datapath):
    pathham = datapath + '/ham'
    pathspam = datapath + '/spam'
    dirham = os.listdir(pathham)
    dirspam = os.listdir(pathspam)
    sectionspam = ""
    sectionham = ""
    keys = weightVector.keys()
    hamcorrect = 0
    hamwrong = 0
    spamcorrect = 0
    spamwrong = 0
    for file in dirham:
        hamfilePath = pathham + '/' + file
        f = open(hamfilePath, 'r')
        sectionread = f.read()
        regex = re.compile('\\W*')
        hamtokens = regex.split(sectionread)
        hamtokensList = [singleToken.lower() for singleToken in hamtokens if len(singleToken) > 1]
        sum = 0
        store = {}
        for token in hamtokensList:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0

        f.close()
        for token in hamtokensList:
            if weightVector.has_key(token):
                sum+=weightVector[token]*store[token]
        sum =calcSigmoid(sum)
        if sum > 0.5:
            hamcorrect += 1
        else:
            hamwrong += 1

    print "correct",hamcorrect
    print "wrong",hamwrong


    for file in dirspam:
        spamfilePath = pathspam + '/' + file
        f = open(spamfilePath, 'r')
        sectionread = f.read()
        regex = re.compile('\\W*')
        spamtokens = regex.split(sectionread)
        spamtokensList = [singleToken.lower() for singleToken in spamtokens if len(singleToken) > 1]
        sum = 0
        store = {}
        for token in spamtokensList:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0

        f.close()
        for token in spamtokensList:
            if weightVector.has_key(token):
                sum+=weightVector[token]*store[token]
        sum =calcSigmoid(sum)
        if sum <= 0.5:
            spamcorrect += 1
        else:
            spamwrong += 1

    print "correct",spamcorrect
    print "wrong",spamwrong

if __name__ == "__main__":
    stopWords = "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/stopwords.txt"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train")
    gradientDescent()
    test("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_test/test/")
