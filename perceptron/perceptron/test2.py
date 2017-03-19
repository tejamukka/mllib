#import numpy as np
import os
import re
import math
import random

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
eta = 0.05
lamda = 3.5
totalTokens =[]

global hamcorrect
global hamwrong
global spamcorrect
global spamwrong

def getAllWords(datapath,stopwordsPath=None):
    pathtrain = datapath
    dirtrain = os.listdir(pathtrain)
    sectiontrain =""
    spamData = []
    stopWords = []
    if stopwordsPath is not None:
        f = open(stopwordsPath, 'r')
        regex = re.compile('\\W*')
        stopWords = regex.split(f.read())
        f.close()
    for file in dirtrain:
        trainfilePath = pathtrain +'/' + file
        f=open(trainfilePath,'r')
        sectiontrain = f.read()
        #sectiontrain += sectionread
        regex = re.compile('\\W*')
        traintokens = regex.split(sectiontrain)
        traintokensList = [singleToken.lower() for singleToken in traintokens if (len(singleToken) >1 and singleToken not in stopWords)]
        store = {}
        error = 0
        for token in traintokensList:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0
            if not (token in totalTokens):
                totalTokens.append(token)


            if not weightVector.has_key(token):
                weightVector[token] = random.uniform(-1,1)
        if "ham" in file:
            fileData.append({'fileName':file,'text':sectiontrain,'fileTokens':store,'class':1})
        else:
            fileData.append({'fileName': file, 'text': sectiontrain, 'fileTokens': store, 'class': 0})
        f.close()
    perceptronTrain()


def perceptronTrain():
    #print weightVector
    for i in range(1,500):
        updateWeights()
   # print("done")
    #print weightVector

def updateWeights():
    change =0
    for eachFile in fileData:
        tokens = eachFile["fileTokens"]
        trueValue = eachFile["class"]
        sum = 0.5
        for token in tokens:
            if weightVector.has_key(token):
                sum += tokens[token] * weightVector[token]
        if(sum >0):
            sum =1
        else:
            sum =-1
        for token1 in tokens:
            if weightVector.has_key(token1):
                weightVector[token1] += (eta)*(trueValue -sum)*(tokens[token1])
    for eachFile in fileData:
        tokens = eachFile["fileTokens"]
        trueValue = eachFile["class"]
        sum = 0.5
        for token in tokens:
            if weightVector.has_key(token):
                sum += tokens[token] * weightVector[token]
        if (sum > 0):
            change += trueValue - 1
        else:
            change += -trueValue + 0

        #weightVector[token] += (eta) * (trueValue - sum)
        #print weightVector["name"]
        #if tokens.has_key(token):
             #  sum +=tokens[token]*(trueValue-eachFile["error"])



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
        hamtokensList = [singleToken.lower() for singleToken in hamtokens if (len(singleToken) >1 and singleToken not in stopWords)]
        sum = 0.5
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
                #sum += weightVector[token]
        #sum =calcSigmoid(sum)
        if sum >= 0:
            hamcorrect += 1
        else:
            hamwrong += 1
    totalhamcount = hamcorrect+hamwrong
    # print "totalhamcount",hamcorrect
    # print "hamcorrect", hamcorrect
    # print "hamwrong",hamwrong


    for file in dirspam:
        spamfilePath = pathspam + '/' + file
        f = open(spamfilePath, 'r')
        sectionread = f.read()
        regex = re.compile('\\W*')
        spamtokens = regex.split(sectionread)
        spamtokensList = [singleToken.lower() for singleToken in spamtokens if (len(singleToken) >1 and singleToken not in stopWords)]
        sum = 0.5
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
                 #sum += weightVector[token]
        #sum =calcSigmoid(sum)
        if sum <= 0:
            spamcorrect += 1
        else:
            spamwrong += 1
#    print "spamcorrect", spamcorrect

    # print "spamcorrect",spamcorrect
    # print "spamwrong",spamwrong
    # print (hamcorrect+spamcorrect)/(hamcorrect+spamcorrect+hamwrong+spamwrong) ,"accuracy "
    return hamcorrect, hamwrong, spamcorrect, spamwrong



if __name__ == "__main__":
    #stopWords = "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/stopwords.txt"
    #getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train", stopWords)
    stopWords = "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/stopwords.txt"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/hw2_train/train/three")
    result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/hw2_test/test")

    print "hw2_test_data_accuracy"
    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    #print sum
    tsum = result[0] + result[2] + result[1] + result[3]
    #print tsum
    print  (sum / float(tsum)) * 100, "total accuracy"

    print "_______________________________________________________________________________________________________________________________________-"

    print "enron1_test_set_accuracy"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron1_train/enron1/train/third")
    result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron1_test/enron1/test")

    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    # print sum
    tsum = result[0] + result[2] + result[1] + result[3]
    # print tsum
    print  (sum / float(tsum)) * 100, "total accuracy"


    print "_______________________________________________________________________________________________________________________________________-"
    print "enron4_test_set_accuracy"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_train/enron4/train/third")
    result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_test/enron4/test")

    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    # print sum
    tsum = result[0] + result[2] + result[1] + result[3]
    # print tsum
    print  (sum / float(tsum)) * 100, "total accuracy"

    #    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_train/enron4/train")
    #   result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_test/enron4/test")


    print "_______________________________________________________________________________________________________________________________________-"
    print "hw2_test_data_accuracy without stopwords"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/hw2_train/train/three",stopWords)
    result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/hw2_test/test")

    print "hw2_test_data_accuracy without stopwords"
    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    # print sum
    tsum = result[0] + result[2] + result[1] + result[3]
    # print tsum
    print  (sum / float(tsum)) * 100, "total accuracy"

    print "_______________________________________________________________________________________________________________________________________-"

    print "enron1_test_set_accuracy without stopwords"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron1_train/enron1/train/third",stopWords)
    result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron1_test/enron1/test")

    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    # print sum
    tsum = result[0] + result[2] + result[1] + result[3]
    # print tsum
    print  (sum / float(tsum)) * 100, "total accuracy"

    print "_______________________________________________________________________________________________________________________________________-"
    print "enron4_test_set_accuracy without stopwords"
    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_train/enron4/train/third",stopWords)
    result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_test/enron4/test")

    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    # print sum
    tsum = result[0] + result[2] + result[1] + result[3]
    # print tsum
    print  (sum / float(tsum)) * 100, "total accuracy"

    #    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_train/enron4/train")
    #   result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_test/enron4/test")


    print "_______________________________________________________________________________________________________________________________________-"
