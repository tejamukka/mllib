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
lamda = 3.5


global hamcorrect
global hamwrong
global spamcorrect
global spamwrong

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
    for i in range(1,100):
        err= updateError()
       # if(err < 310 and err > 290):
        #    break
        updateWeights()

def updateError():
    error=0
    for eachFile in fileData:
        keys = eachFile["fileTokens"]
        sum = 0
        for token in keys:
            sum += keys[token]*weightVector[token]
        eachFile["error"] = calcSigmoid(sum)
        error+= eachFile["error"]
    print error
    return error
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
    hamcorrect=0
    spamcorrect=0
    hamwrong=0
    spamwrong=0
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
    totalhamcount = hamcorrect+hamwrong
    print "totalhamcount",hamcorrect
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
    return hamcorrect,hamwrong,spamcorrect,spamwrong
    #print (hamcorrect+spamcorrect)/(hamcorrect+spamcorrect+hamwrong+spamwrong) ,"accuracy "

if __name__ == "__main__":
    stopWords = "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/stopwords.txt"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train",stopWords)
    gradientDescent()
    result = test("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_test/test/")
    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    print sum
    tsum = result[0] + result[2]  +result[1] + result[3]
    print tsum
    
    print  sum/tsum, "total accuracy"