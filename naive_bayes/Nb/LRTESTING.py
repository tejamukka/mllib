import numpy as np
import os
import re
import math
spamwordsList=[]

hamwordList=[]
fileTokenMap={}
weightsMap ={}
testfileTokenMap={}
testweightsMap ={}
evalHypMap={}
testevalHypMap={}

def calcSigmoid(z):
    denom = 1+np.exp(-z)
    #print 1/denom
    return 1/denom


def getAllWords(datapath):
    #global words
    pathham = datapath +'/ham'
    pathspam = datapath +'/spam'
    dirham = os.listdir(pathham)
    dirspam = os.listdir(pathspam)
    words=[]
    sectionspam =""
    sectionham =""
    hamtokensList=[]
    spamtokensList=[]
    arr2=[]
    for file in dirham:
        hamfilePath = pathham +'/' + file
        f=open(hamfilePath,'r')
        sectionread = f.read()
        sectionham+=sectionread
        sectionham = sectionham.replace('\n',' ')
        regex = re.compile('\\W*')
        hamtokens = regex.split(sectionham)
        hamtokensList = [singleToken.lower() for singleToken in hamtokens if len(singleToken) >1]
        arr = np.array(hamtokensList).tolist()

        store = {}
        for token in arr:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0
        fileTokenMap[file] =store

    for file in dirspam:
        spamfilePath = pathspam + '/' + file
        f = open(spamfilePath, 'r')
        sectionread = f.read()
        sectionspam+=sectionread
        regex =  re.compile('\\W*')
        spamtokens= regex.split(sectionspam)
        spamtokensList = [singleToken.lower() for singleToken in spamtokens if len(singleToken) > 1]
        arr = np.array(spamtokensList).tolist()
        store = {}
        for token in arr:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0
        fileTokenMap[file] = store

    totalsection = sectionham + sectionspam
    regex = re.compile('\\W*')
    alltokens = regex.split(totalsection)
    alltokensList = [singleToken.lower() for singleToken in alltokens if len(singleToken) > 1]
    alltokenset = set(alltokensList)
    alltokensList = list(alltokenset)
    for token in alltokensList:
        weightsMap[token] =0.5
    return alltokensList


getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train")



print weightsMap


def evaluateHypothesis(fileName):
    sum =1
    if(fileTokenMap.has_key(fileName)):
        fileTokens =fileTokenMap[fileName]
        for key in fileTokens.keys():
            if(weightsMap.has_key(key)):
                #sum+= fileTokens[key]*weightsMap[key]
                sum +=  weightsMap[key]
    sigmoidvalue = calcSigmoid(sum)

    return sigmoidvalue

def ErrorOfEachFile(filename):
    hypo = evaluateHypothesis(file)
    if ("ham" in filename):
        error = math.log(hypo,10)
    else:
        error = math.log(1-hypo,10)
    return error


def totalErrorCalc():
    totalErr =0
    for file in fileTokenMap:
        #print file
        totalErr+=ErrorOfEachFile(file)
    print totalErr,"total"
    return totalErr

#totalErrorCalc()

def Error_Function_Change(eta,featureIndex):
    sumError =0

    for file in fileTokenMap:
        fileTokens = fileTokenMap[file]
        if ("ham" in file):
            Y=1
        else:
            Y=0

        #hypothesis = evaluateHypothesis(file)
        hypothesis = evalHypMap[file]
        #error =0
        if(fileTokens.has_key(featureIndex)):
            error =(-hypothesis+Y)*(fileTokens[featureIndex])
            sumError+= error
    totalError = eta*sumError
    return totalError

def calEvalHypothesis():
    for file in fileTokenMap:
        eachHypo = evaluateHypothesis()
        evalHypMap[file] =eachHypo


def gradientDescent(eta,lamda):
    for weight in weightsMap:
        #print weight
        weightchange = Error_Function_Change(0.01,weightsMap[weight])
        #print weight,weightsMap[weight],weightchange ,"weight","value","weightchange"
       # print weightchange,"weightchange" ,w   eight
        weightsMap[weight] += weightchange - (weightsMap[weight]*eta*lamda)
        #print weightsMap[weight],"after"
    return weightsMap





def testevaluateHypothesis(fileName):
 #   print fileTokenMap
    sum =1
    #print weightsMap
    if(testfileTokenMap.has_key(fileName)):
        testfileTokens =testfileTokenMap[fileName]
        for key in testfileTokens.keys():
            if(weightsMap.has_key(key)):
                sum+= testfileTokens[key]*weightsMap[key]
    sigmoidvalue = calcSigmoid(sum)

     #   print sigmoidvalue
    return sigmoidvalue
    # q=p['for']


def testcalEvalHypothesis():
    for file in testfileTokenMap:
        eachHypo = testevaluateHypothesis()
        testevalHypMap[file] =eachHypo


def getAllWordsTest(datapath):
    # global words
    pathham = datapath + '/ham'
    pathspam = datapath + '/spam'
    dirham = os.listdir(pathham)
    dirspam = os.listdir(pathspam)
    words = []
    sectionspam = ""
    sectionham = ""
    hamtokensList = []
    spamtokensList = []
    arr2 = []
    for file in dirham:
        hamfilePath = pathham + '/' + file
        f = open(hamfilePath, 'r')
        sectionread = f.read()
        sectionham += sectionread
        sectionham = sectionham.replace('\n', ' ')
        regex = re.compile('\\W*')
        hamtokens = regex.split(sectionham)
        # hamtokens = re.split(' ',sectionread)
        # hamtokens = re.split('\n', sectionread)
        hamtokensList = [singleToken.lower() for singleToken in hamtokens if len(singleToken) > 1]
        arr = np.array(hamtokensList).tolist()
        store = {}
        for token in arr:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0
        testfileTokenMap[file] = store

    for file in dirspam:
        spamfilePath = pathspam + '/' + file
        f = open(spamfilePath, 'r')
        sectionread = f.read()
        sectionspam += sectionread
        regex = re.compile('\\W*')
        spamtokens = regex.split(sectionspam)
        spamtokensList = [singleToken.lower() for singleToken in spamtokens if len(singleToken) > 1]
        arr = np.array(spamtokensList).tolist()
        store = {}
        for token in arr:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0
        testfileTokenMap[file] = store

    totalsection = sectionham + sectionspam
    regex = re.compile('\\W*')
    alltokens = regex.split(totalsection)
    return totalsection


def  Test():
    getAllWordsTest("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_test/test")

    hamsuccesscount=0
    hamfailurecount=0
    spamsuccesscount=0
    spamfailurecount=0
    hamcount=0
    spamcount=0
    print weightsMap
    for file in testfileTokenMap:
        #hypo =testevaluateHypothesis(file)
        hypo = testevaluateHypothesis(file)
        if ("ham" in file):
            hamcount+=1
            if(hypo >0.5):
                hamsuccesscount+=1
            else:
                hamfailurecount+=1
        else:
            spamcount+=1
            if(hypo<0.5):
                spamsuccesscount+=1
            else:
                spamfailurecount+=1

    print hamsuccesscount ,"hamsucces"
    print hamfailurecount,"hamfailure"
    print spamsuccesscount,"spamsuccess"
    print spamfailurecount,"spamfailure"
    print hamcount,"hamcount"
    print spamcount,"spamcount"



calEvalHypothesis()
print"call has been done"
for x in range(0,50):

    gradientDescent(0.01,3.5)
Test()
