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


def perceptronTrain():
    keys = weightVector.keys()
    for i in range(1,1000):
        updateWeights()
    print("done")

def updateWeights():
    #keys = weightVector.keys()
    for eachFile in fileData:
        tokens = eachFile["fileTokens"]
        trueValue = eachFile["class"]
        sum = -2.5
        for token in tokens:
            if weightVector.has_key(token):
                sum += tokens[token] * weightVector[token]
        if(sum >0):
            sum =1
        else:
            sum =-1
        for token in tokens:
            weightVector[token] += (eta)*(trueValue -sum)*(tokens[token])
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
        hamtokensList = [singleToken.lower() for singleToken in hamtokens if len(singleToken) > 1]
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
        #sum =calcSigmoid(sum)
        if sum >= 0:
            hamcorrect += 1
        else:
            hamwrong += 1
    totalhamcount = hamcorrect+hamwrong
    print "totalhamcount",hamcorrect
    print "hamcorrect", hamcorrect
    print "hamwrong",hamwrong


    for file in dirspam:
        spamfilePath = pathspam + '/' + file
        f = open(spamfilePath, 'r')
        sectionread = f.read()
        regex = re.compile('\\W*')
        spamtokens = regex.split(sectionread)
        spamtokensList = [singleToken.lower() for singleToken in spamtokens if len(singleToken) > 1]
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
        #sum =calcSigmoid(sum)
        if sum <= 0:
            spamcorrect += 1
        else:
            spamwrong += 1
#    print "spamcorrect", spamcorrect

    print "spamcorrect",spamcorrect
    print "spamwrong",spamwrong
    print (hamcorrect+spamcorrect)/(hamcorrect+spamcorrect+hamwrong+spamwrong) ,"accuracy "
    return hamcorrect, hamwrong, spamcorrect, spamwrong


#getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/hw2_train/train")

if __name__ == "__main__":
    #stopWords = "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/stopwords.txt"
    #getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train", stopWords)
    getAllWords("assignment3/hw2_train/train")
    result = test("assignment3/hw2_train/train/")
#    getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_train/enron4/train")
 #   result = test("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/enron4_test/enron4/test")


    print result[0], "ham successsfully classified"
    print result[1], "ham successsfully not classified"
    print result[2], "spam successsfully classified"
    print result[3], "spam successsfully not classified"
    sum = result[0] + result[2]
    print sum
    tsum = result[0] + result[2] + result[1] + result[3]
    print tsum

    print  (sum / float(tsum))*100, "total accuracy"
