#import numpy as np
import os
import re
import math
#from pandas import  DataFrame
#import numpy
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.neural_network import MLPClassifier
testfinalList =[]
finalList =[]
wordsList = {}

spamwordsList=[]
hamwordList=[]
fileTokenMap={}
weightsMap ={}
testfileTokenMap={}
testweightsMap ={}
totaltokens ={}
testtotaltokens ={}
totaltokensList =[]
testtotaltokensList =[]

fileData = []
testfileData = []
tokenCountMap = {}
weightVector={}
eta = .01
lamda = 3.5
classList =[]
testclassList =[]

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
           #totaltokens
           if (totaltokens.has_key(token)):
                totaltokens[token] = token

           else:
                totaltokens[token] = token
           if (store.has_key(token)):
               store[token] += 1.0
           else:
               store[token] = 1.0

           if not weightVector.has_key(token):
                weightVector[token] = 0

        fileData.append({'fileName':file,'text':sectionread,'fileTokens':store,'classVal':1})
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
            if (totaltokens.has_key(token)):
                totaltokens[token] = token
            else:
                totaltokens[token] = token


            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0


            if not weightVector.has_key(token):
                weightVector[token] = 0

        fileData.append({'fileName':file,'text':sectionread,'fileTokens':store,'classVal':0})
        f.close()
    for allToken in totaltokens.keys():
        totaltokensList.append(totaltokens[allToken])
    #print totaltokensList
    #print  totaltokensList.__len__()
    for eachfile in fileData:
        filevect =[0]*5839
        i =-1
        for totaltoken in totaltokensList:
            i+=1
            filetokens = eachfile["fileTokens"]
            if filetokens.has_key( totaltoken):
                    filevect[i] = filetokens[totaltoken]
        finalList.append(filevect)
        classList.append(eachfile["classVal"])

    #print finalList[0]
    #print classList
    #print "done"
    # clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    # clf.fit(finalList, classList)
    # MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',
    #               beta_1=0.9, beta_2=0.999, early_stopping=False,
    #               epsilon=1e-08, hidden_layer_sizes=(5, 2), learning_rate='constant',
    #               learning_rate_init=0.001, max_iter=200, momentum=0.9,
    #               nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
    #               solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
    #               warm_start=False)


def Test(datapath,stopwordsPath=None):
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
           #totaltokens
           if (testtotaltokens.has_key(token)):
                testtotaltokens[token] = token

           else:
                testtotaltokens[token] = token
           if (store.has_key(token)):
               store[token] += 1.0
           else:
               store[token] = 1.0


        testfileData.append({'fileName':file,'text':sectionread,'fileTokens':store,'classVal':1})
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
            if (totaltokens.has_key(token)):
                testtotaltokens[token] = token
            else:
                testtotaltokens[token] = token


            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0


            if not weightVector.has_key(token):
                weightVector[token] = 0

        testfileData.append({'fileName':file,'text':sectionread,'fileTokens':store,'classVal':0})
        f.close()
    for allToken in totaltokens.keys():
        testtotaltokensList.append(totaltokens[allToken])
    #print testtotaltokensList
    #print  testtotaltokensList.__len__()
    for eachfile in testfileData:
        testfilevect =[0]*5839
        i =-1
        for totaltoken in testtotaltokensList:
            i+=1
            filetokens = eachfile["fileTokens"]
            if filetokens.has_key( totaltoken):
                    testfilevect[i] = filetokens[totaltoken]
        testfinalList.append(testfilevect)
        testclassList.append(eachfile["classVal"])


    for testFile in testfinalList:
        cnt = 0
        for test in testFile:
            if not test == 0:
                cnt += 1
        print cnt, "cnt"
    print testfinalList[0]
    print testfinalList[1]
    #print testclassList
    #print "done"
    #
    # clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    # clf.fit(finalList, classList)
    # MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',
    #               beta_1=0.9, beta_2=0.999, early_stopping=False,
    #               epsilon=1e-08, hidden_layer_sizes=(5, 2), learning_rate='constant',
    #               learning_rate_init=0.001, max_iter=200, momentum=0.9,
    #               nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
    #               solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
    #               warm_start=False)
    # res =clf.predict(testfinalList)
    # print res
    #
    #




#getAllWords("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/hw2_train/train/")
getAllWords("assignment3/hw2_train/train/")
Test("assignment3/hw2_test/test/")

























   # perceptronTrain()
   # build_data_frame('','')

# def build_data_frame(path, classification):
#     rows = []
#     index = []
#     for data in fileData:
#         rows.append({'text': data.text, 'class': data.classVal})
#         index.append(data.fileName)
#
#     data_frame = DataFrame(rows, index=index)
#     return data_frame
#
# data = DataFrame({'text': [], 'class': []})
# data = data.append(build_data_frame('',''))
# data = data.reindex(numpy.random.permutation(data.index))
#
# count_vectorizer = CountVectorizer()
# counts = count_vectorizer.fit_transform(data['text'].values)
#
# classifier = MultinomialNB()
# targets = data['class'].values
# classifier.fit(counts, targets)
#
#
# if __name__ == "__main__":
#     getAllWords("assignment3/hw2_train/train")
#
