from __future__ import division
import os
import re
import numpy as np
import time
from math import log


allTrainingFilesList=[]
classDocsCount={}
classTextSection={}
classWordsCount={}
priorClass={}
classTokensCount={}
classCondProbMap={}

#textsection=""
#     N = ExtractDocs(D)
#     for class in Class:
#         Nc = CountDocsInClass(D,class)
#         classText = ConcatenateTextOfAllDocsInClass(D,C)
#         for token in V:
#             count[class][token] = CountTokensOfTerm(classtext,token)
#         for token in V:
#             condProb[class][token] = count[class][token]/totalCount[class][token]
#
#

def AppendAllDocs(datasetPath):
    path = datasetPath
    pathham = datasetPath+'/' +'ham'
    pathspam = datasetPath + '/' + 'spam'
    dirham = os.listdir(pathham)
    dirspam = os.listdir(pathspam)
    hamfilecount =0
    spamfilecount =0
    hamtextsection=""
    spamtextsection =""
    for file in dirham:
        hamfilecount += 1
        hamFilesPath = pathham + '/' + file
        allTrainingFilesList.extend(file)
        f = open(hamFilesPath, 'r')
        hamtextsection += f.read()
    for file in dirspam:
        spamfilecount += 1
        spamFilesPath = pathspam + '/' + file
        allTrainingFilesList.extend(file)
        f = open(spamFilesPath, 'r')
        spamtextsection += f.read()
    totaltextsection = hamtextsection + spamtextsection
    classDocsCount["ham"]=hamfilecount
    classDocsCount["spam"] =spamfilecount
    totalfilecount = hamfilecount + spamfilecount
    classDocsCount["total"] = totalfilecount
    classTextSection["ham"] = hamtextsection
    classTextSection["spam"] = spamtextsection
    classTextSection["total"] =  totaltextsection
    return totaltextsection,hamtextsection,spamtextsection,allTrainingFilesList,hamfilecount,spamfilecount,totalfilecount

def ExtractVocabulary(DataSet):
    result = AppendAllDocs(DataSet)
    totaltext = result[0]
    hamtotaltext=result[1]
    spamtotaltext=result[2]

    tokenList = re.split(' ', totaltext)
    totalwordList = [singleToken.lower() for singleToken in tokenList if len(singleToken) > 1]

    hamtokenList = re.split(' ', hamtotaltext)
    hamwordList = [singleToken.lower() for singleToken in hamtokenList if len(singleToken) > 1]

    spamtokenList = re.split(' ', spamtotaltext)
    spamwordList = [singleToken.lower() for singleToken in spamtokenList if len(singleToken) > 1]
    classWordsCount["ham"] =hamwordList
    classWordsCount["spam"] =spamwordList
    classWordsCount["total"] = totalwordList
    return totalwordList,hamwordList,spamwordList


def TrainMultinomialNB(ClassName,Data):
    VocabList = ExtractVocabulary(Data)
    totalVocabList =VocabList[0]
    # totalVocabList = totalVocabList
    # print totalVocabList.__len__(),"first"
    # totalVocabListSet = set(totalVocabList)
    # print totalVocabList.__len__(),"midde;"
    # totalVocabUniquetokensList = list(totalVocabList)
    # print totalVocabUniquetokensList.__len__(),"unique"
    hamVocabList = VocabList[1]
    spamVocabList = VocabList[2]
    docs=   AppendAllDocs(Data)
    N = docs[6]
    print "i am here1"
    tokenscount={}
    totaltokensSum={}
    tsum =0
    tsummap={}
    condProbMap={}
    print "i am here2"
    for cls in ClassName:
        NC = classDocsCount[cls]
        priorClass[cls] = NC/N
        textofEachClass = classTextSection[cls]
        print "i am here3"
        for token in totalVocabList:
            count =0
            for classtoken in classWordsCount[cls]:
                if token == classtoken:
                  count+=1
            if tokenscount.has_key(token):
                 a = "do nothing"
            else:
                tokenscount[token]= count
        classTokensCount[cls] =tokenscount
        print "i am here4"
        for token in totalVocabList: #for the denominator sum
            clstokencountmap = classTokensCount[cls]
            tsum += clstokencountmap[token] + 1
        totaltokensSum[cls] = tsum

        for token in totalVocabList:
            clstkncountmap = classTokensCount[cls]
            condProb = (clstkncountmap[token]+1)/totaltokensSum[cls]
            condProbMap[token] = condProb
        classCondProbMap[cls] =condProbMap
        print priorClass
    print classCondProbMap["ham"]
    print classCondProbMap["spam"]
    return totalVocabList,priorClass,classCondProbMap


#TrainMultinomialNB()


    #     for class in Class:
    #         Nc = CountDocsInClass(D,class)
    #         classText = ConcatenateTextOfAllDocsInClass(D,C)
    #         for token in V:
    #             count[class][token] = CountTokensOfTerm(classtext,token)
    #         for token in V:
    #             condProb[class][token] = count[class][token]/totalCount[class][token]
    #
className = ["ham","spam"]
TrainMultinomialNB(className,"C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/")

#ExtractVocabulary("C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/")



