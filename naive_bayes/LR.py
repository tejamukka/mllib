import numpy as np
import os
import re
import math
spamwordsList=[]

hamwordList=[]
fileTokenMap={}
weightsMap ={}

def calcSigmoid(z):
    denom = 1+np.exp(-z)
    #print 1/denom
    return 1/denom
calcSigmoid(1000)



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
        #hamtokens = re.split(' ',sectionread)
       # hamtokens = re.split('\n', sectionread)
        hamtokensList = [singleToken.lower() for singleToken in hamtokens if len(singleToken) >1]
        arr = np.array(hamtokensList).tolist()
        store = {}
        for token in arr:
            if (store.has_key(token)):
                store[token] += 1.0
            else:
                store[token] = 1.0
        fileTokenMap[file] =store

    # p =fileTokenMap[file]
    # q=p['for']
    # print q,"hey"
    #print hamtokensList.__len__()
    for file in dirspam:
        spamfilePath = pathspam + '/' + file
        f = open(spamfilePath, 'r')
        sectionread = f.read()
        sectionspam+=sectionread
        regex =  re.compile('\\W*')
        spamtokens= regex.split(sectionspam)
        #spamtokens =sectionspam.replace('\n',' ')
        #spamtokens = re.split(' ', sectionread)
        #spamtokens = re.split('\n', sectionread)
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
    #alltokens = re.split(' ', totalsection)
    #alltokens = re.split('\n', totalsection)
    alltokensList = [singleToken.lower() for singleToken in alltokens if len(singleToken) > 1]
    alltokenset = set(alltokensList)
    alltokensList = list(alltokenset)
    for token in alltokensList:
        weightsMap[token] =0
    return alltokensList


getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train")


def evaluateHypothesis(fileName):
 #   print fileTokenMap
    sum =0
    if(fileTokenMap.has_key(fileName)):
        fileTokens =fileTokenMap[fileName]
    #fileTokens.replace('\n','')
    #print fileTokens

        for key in fileTokens.keys():
            if(weightsMap.has_key(key)):
                sum+= fileTokens[key]*weightsMap[key]
        sigmoidvalue = calcSigmoid(sum)

     #   print sigmoidvalue
    return calcSigmoid(sum)
    # q=p['for']
    #
    # for index in weights:
    #     sum+= weights[index]*features[index]
    # return calcSigmoid(sum)

def ErrorOfEachFile(filename):
    #features = getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train")
    hypo = evaluateHypothesis(file)
    if ("ham" in filename):
        error = math.log(hypo,10)
    else:
        error = math.log(1-hypo,10)
    return error


def totalError():
    totalErr =0
    for file in fileTokenMap:
        print file
        totalErr+=ErrorOfEachFile(file)
    #print totalErr,"total"
    return totalErr

totalError()

def Error_Function_Change(eta,featureIndex):
    sumError =0

    for file in fileTokenMap:
        fileTokens = fileTokenMap[file]
        if ("ham" in file):
            Y=1
        else:
            Y=0

        hypothesis = evaluateHypothesis(file)
        if(fileTokens.has_key(featureIndex)):
            error =(hypothesis-Y)*(fileTokens[featureIndex])
    sumError+= error
    totalError = eta*sumError
    print totalError ,"tracking the error"
    return totalError

def gradientDescent(eta,lamda):

    for weight in weightsMap:
        weightchange = Error_Function_Change(0.001,weight)
        weightsMap[weight] = [weightsMap[weight]*(1-eta*lamda)] + weightchange
    return 1

for x in xrange(100):
    gradientDescent(0.001,0.35)
   # print totalError()
    #Error_Function_Change()

#Error('','')













    # pathham = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham'
    # dirham = os.listdir(pathham)
    # errorSum = 0
    # errorSumHam=0
    # errorSumSpam =0
    # for file in dirham:
    #     error = eachFileSigmoid(file)
    #     if error!=0:
    #         errorSumHam+= 1*math.log(error,10)
    #
    # pathspam = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam'
    # dirspam = os.listdir(pathspam)
    # for file in dirspam:
    #     error = eachFileSigmoid(file)
    #     if error!=1:
    #         errorSumSpam+= 1*math.log(1-error,10)
    # return errorSumHam +errorSumSpam
    #
    #
    #

        #weightsMap[token]=1
        #fileTokenMap[file] = spamtokensList
    #print spamtokensList.__len__()
    # words=hamtokensList+spamtokensList
    # wordsset = set(words)
    # wordsArray = np.asarray(list(wordsset))
    # for token in wordsArray:
    #     weightsMap[token]=.5
    #     #print weightsMap


    # totalsection = sectionham + sectionspam
    # alltokens = re.split(' ',totalsection)
    # alltokensList = [singleToken.lower() for singleToken in alltokens if len(singleToken) > 1]
    # alltokenset = set(alltokensList)
    # alltokensList = list(alltokenset)


    #alltokenArray = np.array(list(alltokenset))
    #print hey
   # print fileTokenMap
   #  print fileTokenMap
   #  print alltokensList
   #  return alltokensList













#
# def ErrorHam(features,weights):
#     print "error ham"
#     features = getAllWords("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train")
#     pathham = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham'
#     dirham = os.listdir(pathham)
#     errorSum = 0
#     errorSumHam=0
#     errorSumSpam =0
#     for file in dirham:
#         error = eachFileSigmoid(file)
#         if error!=0:
#             errorSumHam+= 1*math.log(error,10)
#
#     pathspam = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam'
#     dirspam = os.listdir(pathspam)
#     for file in dirspam:
#         error = eachFileSigmoid(file)
#         if error!=1:
#             errorSumSpam+= 1*math.log(1-error,10)
#     return errorSumHam +errorSumSpam
#
#
#
# def eachFileSigmoid(fileName):
#     fileTokens = fileTokenMap[fileName]
#     weightsum = 0
#     token_num = 1
#     for token in fileTokens:
#         if (weightsMap.has_key(token)):
#             weightsum += token_num * (weightsMap[token])
#         else:
#             weightsum += 0.0
#     hyp = calcSigmoid(weightsum)
#     #errorsum = 1*math.log(hyp,10)
#     return hyp
#
#
#
#
# ErrorHam('', '')
#
#
























































    #
    # dirham = os.listdir(pathham)
    # for file in dirham:
    #     hamfilePath = pathham + '/' + file
    #     f = open(hamfilePath, 'r')
    #     sectionread = f.read()
    #     hamtokens = re.split(' ', sectionread)
    #     hamtokensList = [singleToken.lower() for singleToken in hamtokens if len(singleToken) > 1]
    #     fileTokenMap[file] = hamtokensList
    #






#
# def getAllWords(datapath):
#     global words
#     pathham = datapath +'/ham'
#     pathspam = datapath +'/spam'
# #    print pathspam
#     dirham = os.listdir(pathham)
#     dirspam = os.listdir(pathspam)
#     words=[]
#     for file in dirham:
#         hamfilePath = pathham +'/' + file
#         #print hamfilePath
#         f=open(hamfilePath,'r')
#         sectionread = f.read()
#         hamtokens = re.split(' ',sectionread)
#         hamtokensList = [singleToken.lower() for singleToken in hamtokens if len(singleToken) >1]
#     print hamtokensList.__len__()
#     #print hamtokensList
#
#     for file in dirspam:
#         spamfilePath = pathspam + '/' + file
#         # print hamfilePath
#         f = open(spamfilePath, 'r')
#         sectionread = f.read()
#         spamtokens = re.split(' ', sectionread)
#         spamtokensList = [singleToken.lower() for singleToken in spamtokens if len(singleToken) > 1]
#     print spamtokensList.__len__()
#    # print spamtokensList
#     words=hamtokensList+spamtokensList
#    # print words
#     #print words.index('tenaska'),"index"
#     #print words.__len__()
#     #print words
#     wordsset = set(words)
#    # wordsetList = list(wordsset)
#    # print wordsetList('tenaska') ,"index2"
#     #print wordsset.__len__(),"unique"
#     #if isinstance(words,list):
#     #    print "true"
#
#     wordsArray = np.asarray(list(wordsset))
#     print wordsArray
#  #   print len(wordsArray)
#    # print len(wordsArray),"array"
#
#     #return words
#     return wordsArray
#
