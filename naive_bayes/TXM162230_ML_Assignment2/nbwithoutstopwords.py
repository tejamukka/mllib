from __future__ import division
import os
import re
from math import log
import sys
def spamSectionText(className,datapath):
  sectionSpam = " "
  pathspam = datapath
  dirspam = os.listdir(pathspam)
  spamcount =0
  for file in dirspam:
    spamcount +=1
    spamFilesPath = pathspam + '/' + file
    f = open(spamFilesPath, 'r')
    sectionSpam += f.read()
  return spamcount,sectionSpam


def hamSectionText(className,datapath):
  global sectionHam
  sectionHam = " "
  pathham = datapath
  dirham = os.listdir(pathham)
  hamcount=0
  for file in dirham:
      hamcount+= 1
      hamFilesPath = pathham  +'/'+file
      f = open(hamFilesPath,'r')
      sectionHam += f.read()

  return hamcount,sectionHam


def Test(str,stopwordspath):
    tokenList = re.split(' ',str)
    wordList = [singleToken.lower() for singleToken in tokenList if len(singleToken) > 1]
 #   print wordList.__len__(),"before"
    #pathstopwords = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/stopwords.txt'
    pathstopwords = stopwordspath
    f = open(pathstopwords, 'r')
    readwords = f.readlines()
    stopwords =[token.strip() for token in readwords]
    for word in wordList:
          if(word in stopwords):
            wordList.remove(word)
#    print wordList.__len__(),"after"
    #print stopwords[100]
    return wordList


#
# def parseText(str):
#     tokenList = re.split(' ', str)
#     #tokenList = re.split(r'\W*',str)
#     wordList = [singleToken.lower() for singleToken in tokenList if len(singleToken) > 1]
#     return wordList

def condProbHam(sectionHam,stopwordspath):
    global totalHamTokenCount
    totalHamTokenCount = 0
    noshowHamProb =1
    hamWordsList = Test(sectionHam,stopwordspath)
    hamWordKeys ={}
    for word in hamWordsList:
        if(hamWordKeys.has_key(word)):
            hamWordKeys[word] += 1.0
        else:
            hamWordKeys[word] = 1.0
    for key in hamWordKeys.keys():
            #print key, hamWordKeys[key]
        totalHamTokenCount += hamWordKeys[key] + 1.0
    hamProbList = []
    hamProbMap ={}
    for key in hamWordKeys.keys():
        tokenHamProb = (hamWordKeys[key] + 1.0) / totalHamTokenCount
        hamProbMap[key] = tokenHamProb
        hamProbList.append(tokenHamProb)
    noshowHamProb = noshowHamProb/totalHamTokenCount
    return hamWordKeys,hamProbList,hamProbMap,noshowHamProb
#

def condProbSpam(sectionSpam,stopwordspath):
    global totalSpamTokenCount
    totalSpamTokenCount = 0
    noshowSpamProb =1
    spamWordsList = Test(sectionSpam,stopwordspath)
    spamWordKeys ={}
    for word in spamWordsList:
        if(spamWordKeys.has_key(word)):
            spamWordKeys[word] += 1.0
        else:
            spamWordKeys[word] = 1.0

    for key in spamWordKeys.keys():
        totalSpamTokenCount += spamWordKeys[key] +1.0
    spamProbMap ={}
    spamProbList = []
    for key in spamWordKeys.keys():
        tokenSpamProb = (spamWordKeys[key] + 1.0) / totalSpamTokenCount
        spamProbMap[key] = tokenSpamProb
        spamProbList.append(tokenSpamProb)
    noshowSpamProb = noshowSpamProb/totalSpamTokenCount
    return spamWordKeys,spamProbList,spamProbMap,noshowSpamProb

def priorHam(hamdatapath):
  Ham = hamSectionText("ham",hamdatapath)
  hamCount = Ham[0]
  hamText = Ham[1]
  return hamCount,hamText


def priorSpam(spamdatapath):
  spam = spamSectionText("spam",spamdatapath)
  SpamCount = spam[0]
  SpamText = spam[1]
  return SpamCount,SpamText


def TrainSpam(spam,spamdatapath,stopwordspath):
    priorInfo = priorSpam(spamdatapath)
    spamCount = priorInfo[0]
    spamSectionText = priorInfo[1]
    spamWordsList = Test(spamSectionText,stopwordspath)
    spamList = condProbSpam(spamSectionText,stopwordspath)
    spamMap = spamList[2]
    sum =0
    for value in spamList[2]:
        sum+= spamMap[value]
    return spamCount, spamSectionText,spamList[2],spamList[3],spamWordsList.__len__()

def TrainHam(ham,hamdatapath,stopwordspath):
    priorInfo = priorHam(hamdatapath)
    hamCount = priorInfo[0]
    hamSectionText = priorInfo[1]
    hamWordsList = Test(hamSectionText,stopwordspath)
    hamList = condProbHam(hamSectionText,stopwordspath)
    hamMap = hamList[2]
    sum = 0
    for value in hamMap:
        sum += hamMap[value]
    return hamCount, hamSectionText,hamList[2],hamList[3],hamWordsList.__len__()

def TrainMultinomail(ham,hamdatapath,spam,spamdatapath,stopwordspath):
    spamData = TrainSpam(spam,spamdatapath,stopwordspath)
    hamData = TrainHam(ham,hamdatapath,stopwordspath)
    hamcount = hamData[4]
    spamcount = spamData[4]
    print hamcount + spamcount , "total words count"
    totalDocsCount = spamData[0] + hamData[0]
    global spamPrior
    spamPrior= spamData[0]/totalDocsCount
    global hamPrior
    hamPrior = hamData[0]/totalDocsCount
    spamVocab = spamData[1]
    hamVocab = hamData[1]
    spamCondProb = spamData[2]
    hamCondprob = hamData[2]
    return hamVocab,spamVocab, hamPrior,spamPrior,hamCondprob,spamCondProb,hamData[3],spamData[3]

def hamSectionTest(className,datapath,trainhampath,trainspampath,stopwordspath):
  global sectionHamTest
  global hamsuccesscount
  global hamfailurecount
  hamfailurecount=0
  sectionHamTest = " "
  hamsuccesscount = 0
  pathham = datapath
  dirham = os.listdir(pathham)
  hamTestCount=0
  trainparams = TrainMultinomail("ham",trainhampath,"spam",trainspampath,stopwordspath)
  for file in dirham:
      hamTestCount+= 1
      hamFilesPath = pathham  +'/'+file
      f = open(hamFilesPath,'r')
      sectionHamTest = f.read()
      tokens = Test(sectionHamTest,stopwordspath)
      hamscore = log(trainparams[2],10)
      spamscore = log(trainparams[3],10)
      hamcondprob = trainparams[4]
      spamcondprob = trainparams[5]
      hamnoshowprob = trainparams[6]
      spamnoshowprob = trainparams[7]
      for  tokenkey in tokens:
          if hamcondprob.has_key(tokenkey):
               hamscore+= log(hamcondprob[tokenkey],10)
          else:
               hamscore+= log(hamnoshowprob,10)
      for tokenkey in tokens:
          if spamcondprob.has_key(tokenkey):
            spamscore += log(spamcondprob[tokenkey],10)
          else:
            spamscore += log(spamnoshowprob,10)

      if hamscore >= spamscore:
          hamsuccesscount+=1
      else:
          hamfailurecount+=1
  #print hamsuccesscount,hamfailurecount
  return hamsuccesscount,hamfailurecount

def spamSectionTest(className,datapath,trainhampath,trainspampath,stopwordspath):

  global sectionSpamTest
  sectionSpamTest = " "
  global spamsuccesscount
  global spamfailurecount
  spamsuccesscount = 0
  spamfailurecount = 0
  pathname = datapath
  dirspam = os.listdir(pathname)
  spamTestCount=0
  trainparams = TrainMultinomail("ham",trainhampath,"spam",trainspampath,stopwordspath)


  for file in dirspam:
      spamTestCount+= 1
      spamFilesPath = pathname  +'/'+file
      f = open(spamFilesPath,'r')
      sectionSpamTest = f.read()
      #tokens = parseText(sectionSpamTest)
      tokens = Test(sectionSpamTest,stopwordspath)
      hamscore = log(trainparams[2],10)
      spamscore = log(trainparams[3],10)
      hamcondprob = trainparams[4]
      spamcondprob = trainparams[5]
      hamnoshowprob = trainparams[6]
      spamnoshowprob = trainparams[7]
      for  tokenkey in tokens:
          if hamcondprob.has_key(tokenkey):
            hamscore+= log(hamcondprob[tokenkey],10)
          else:
               hamscore+= log(hamnoshowprob,10)
      for tokenkey in tokens:
          if spamcondprob.has_key(tokenkey):
            spamscore += log(spamcondprob[tokenkey],10)
          else:
            spamscore += log(spamnoshowprob,10)
      if hamscore <= spamscore:
          spamsuccesscount+=1
      else:
          spamfailurecount+=1
  #print spamsuccesscount,spamfailurecount
  return spamsuccesscount,spamfailurecount
def main1():

    if len(sys.argv) != 6:

        print("Invalid input arguments. Please specify input as : python finename.py trainhampath trainspampath testhampath testspampath stopwordspath")
        sys.exit(1)

    # read inputs from command line

    trainhampath = sys.argv[1]
    trainspampath = sys.argv[2]
    testhampath =sys.argv[3]
    testspampath = sys.argv[4]
    stopwordspath=sys.argv[5]
    print trainhampath, trainspampath, testhampath,testspampath
    ham = hamSectionTest("", testhampath,trainhampath,trainspampath,stopwordspath)
    spam = spamSectionTest("", testspampath,trainhampath,trainspampath,stopwordspath)
    print ham[0], "ham successsfully classified"
    print ham[1], "ham successsfully not classified"
    print spam[0], "spam successsfully classified"
    print spam[1],"spam successsfully not classified"
    print  (ham[0] + spam[0])/(ham[0] + ham[1]+ spam[0] +spam[1])*100,"total accuracy"

   # "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham"  "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam" "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_test/test/ham" "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_test/test/spam"

if __name__ == "__main__":
	main1()


