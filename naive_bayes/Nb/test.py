from __future__ import division
import os
import re
import time

def spamSectionText(className,data):
  global sectionSpam
  sectionSpam = " "
  pathspam = data
  #pathspam = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam'
  #dirham = os.listdir(pathham)
  dirspam = os.listdir(pathspam)
  #hamcount=0
  spamcount =0
#os.chdir(r'C:/Users/tejamukka/PycharmProjects/Nb')
 #  for file in dirham:
 #      hamcount+= 1
 #      hamFilesPath = pathham  +'/'+file
 #      f = open(hamFilesPath,'r')
 #      sectionHam += f.read()
 # # print sectionHam

  for file in dirspam:
    spamcount +=1
    spamFilesPath = pathspam + '/' + file
    f = open(spamFilesPath, 'r')
    sectionSpam += f.read()
  #print sectionSpam
  return spamcount,sectionSpam


def hamSectionText(className,data):
  global sectionHam
  sectionHam = " "
  pathham = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham'
  dirham = os.listdir(pathham)
  hamcount=0
  #os.chdir(r'C:/Users/tejamukka/PycharmProjects/Nb')
  for file in dirham:
      hamcount+= 1
      hamFilesPath = pathham  +'/'+file
      f = open(hamFilesPath,'r')
      sectionHam += f.read()
 # print sectionHam

  return hamcount,sectionHam

def Test(str):
    tokenList = re.split(' ',str)
    wordList = [singleToken.lower() for singleToken in tokenList if len(singleToken) > 1]
    #print wordList.__len__(),"before"
    wordList2 = [singleToken.lower() for singleToken in tokenList if len(singleToken) > 1]
    pathstopwords = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/stopwords.txt'
    f = open(pathstopwords, 'r')
    readwords = f.readlines()
    stopwords =[token.strip() for token in readwords]
    for word in wordList:
        if(word in stopwords):
          wordList.remove(word)
    #print wordList.__len__(),"after"
    #print stopwords[100]
    return wordList



def parseText(str):
    tokenList = re.split(r'\W*',str)
    wordList = [singleToken.lower() for singleToken in tokenList if len(singleToken) > 2]
    #print wordList
    return wordList
#print "ham words"
#parseText(sectionHam)
#print "_----------------------------------------------------------------------------------------------------------------"
#print "spam words"
#parseText(sectionSpam)


def condProbHam(sectionHam):
    global totalHamTokenCount
    totalHamTokenCount = 0
    hamWordsList = parseText(sectionHam)
    #print hamWordsList
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
    for key in hamWordKeys.keys():
        tokenSpamProb = (hamWordKeys[key] + 1.0) / totalSpamTokenCount
      #  print key, tokenSpamProb
        hamProbList.append(tokenSpamProb)
    #print hamProbList
    return hamProbList
    #return tokenHamProb
#
#hamWordsList = parseText(sectionHam)
# for key in hamWordsList:
#     condProbHam(key)

def condProbSpam(sectionSpam):
    global totalSpamTokenCount
    totalSpamTokenCount = 0
    spamWordsList = parseText(sectionSpam)
    #print spamWordsList
    spamWordKeys ={}
    for word in spamWordsList:
        if(spamWordKeys.has_key(word)):
            spamWordKeys[word] += 1.0
        else:
            spamWordKeys[word] = 1.0

    for key in spamWordKeys.keys():
        #print key, spamWordKeys[key]
        totalSpamTokenCount += spamWordKeys[key] +1.0
    spamProbList = []
    for key in spamWordKeys.keys():

        tokenSpamProb = (spamWordKeys[key] + 1.0) / totalSpamTokenCount
       # print key, tokenSpamProb
        spamProbList.append(tokenSpamProb)
  #  print spamProbList
    return spamProbList
#condProbSpam()

#
# spamWordsList = parseText(sectionSpam)
# for key in spamWordsList:
#     condProbSpam(key)


def priorHam():
  Ham = hamSectionText("ham","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham")
  hamCount = Ham[0]
  hamText = Ham[1]
  #totalCount = Count[2]
  #priorHamProb = hamCount / totalCount
  #print priorHamProb
  return hamCount,hamText

#print priorHam() , "ham"

def priorSpam():
  spam = spamSectionText("spam","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam")
  SpamCount = spam[0]
  SpamText = spam[1]
  #totalCount = Count[2]
  #priorSpamProb = SpamCount / totalCount
  #print priorSpamProb
  return SpamCount,SpamText

def TrainSpam(spam,spamDataSet):
    priorInfo = priorSpam()
    spamCount = priorInfo[0]
    spamSectionText = priorInfo[1]
    #spamWordsList = parseText(spamSectionText)
    spamWordsList = Test(spamSectionText)
    spamList = condProbSpam(spamSectionText)
    spamMap = spamList[2]
    #print "hello"
   # print spamMap
    sum =0
    for value in spamList[2]:
        sum+= spamMap[value]
    #print sum,"trainspam"
    #print spamList
    return spamCount, spamSectionText,spamList[2],spamList[3]
# print"spam started"
# TrainSpam("spam","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam")
# print "spam ended"
# print "________________________________________________________________________________________________________________________________________________________________________________________"

def TrainHam(ham,hamDataSet):
    priorInfo = priorHam()
    hamCount = priorInfo[0]
    hamSectionText = priorInfo[1]
    #hamWordsList = parseText(hamSectionText)
    hamWordsList =Test(hamSectionText)
    hamList = condProbHam(hamSectionText)
    hamMap = hamList[2]
    #print "ham_hello"
    sum = 0
    for value in hamMap:
        sum += hamMap[value]
    #print sum,"hamtrain"
   # print hamList
    return hamCount, hamSectionText,hamList[2],hamList[3]
# print"ham started"
# TrainHam("ham","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham")
# print"ham ended"
def TrainMultinomail(ham,spam,hamdata,spamdata):
    #spamData = TrainSpam("spam","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam")
    #hamData = TrainHam("ham","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham")
    spamData = TrainSpam(spam,spamdata )
    hamData = TrainHam(ham,hamdata)
    totalDocsCount = spamData[0] + hamData[0]
    global spamPrior
    spamPrior= spamData[0]/totalDocsCount
    global hamPrior
    hamPrior = hamData[0]/totalDocsCount
    spamVocab = spamData[1]
    hamVocab = hamData[1]
    spamCondProb = spamData[2]
    hamCondprob = hamData[2]
    #print  hamPrior,spamPrior
    return hamVocab,spamVocab, hamPrior,spamPrior,hamCondprob,spamCondProb,hamData[3],spamData[3]
TrainMultinomail("ham","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham","spam","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam")

def hamSectionTest(className,data):
  global sectionHamTest
  global hamsuccesscount
  global hamfailurecount
  hamfailurecount=0
  sectionHamTest = " "
  hamsuccesscount = 0
  pathham = 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_test/test/ham'
  dirham = os.listdir(pathham)
  hamTestCount=0
  #os.chdir(r'C:/Users/tejamukka/PycharmProjects/Nb')
  trainparams = TrainMultinomail("ham","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham","spam","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam")
  for file in dirham:
      hamTestCount+= 1
      hamFilesPath = pathham  +'/'+file
      f = open(hamFilesPath,'r')
      sectionHamTest = f.read()
      #tokens = parseText(sectionHamTest)
      tokens = Test(sectionHamTest)
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
               #hamscore+= hamnoshowprob
         # print hamscore,tokenkey
          #spamscore+= log(spamcondprob[tokenkey])
      for tokenkey in tokens:
          if spamcondprob.has_key(tokenkey):
            spamscore += log(spamcondprob[tokenkey],10)
          else:
            spamscore += log(spamnoshowprob,10)
            #spamscore+=0
        #  print spamscore,tokenkey

      if hamscore >= spamscore:
          hamsuccesscount+=1
      else:
          hamfailurecount+=1
  #print hamsuccesscount,"looking for ham accuracy"
  #print hamfailurecount,"looking for ham failure"
  #print hamsuccesscount/(hamsuccesscount+hamfailurecount), "ham_accuracy"
      #print hamscore,spamscore,"thisoe"
      #print sectionHamTest

  #  hamTestCount,sectionHamTest
  return hamTestCount

note = hamSectionTest("","")
#list = parseText(note[1])
#print list
#def testMultinomialNB():






def spamSectionTest(className,data):
  global sectionSpamTest
  sectionSpamTest = " "
  global spamsuccesscount
  global spamfailurecount
  spamsuccesscount = 0
  spamfailurecount = 0
  pathhame= 'C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_test/test/spam'
  dirham = os.listdir(pathhame)
  spamTestCount=0
  #os.chdir(r'C:/Users/tejamukka/PycharmProjects/Nb')
  trainparams = TrainMultinomail("ham","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham","spam","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/spam")
  #trainparams = TrainMultinomail("ham", "C:/Users/tejamukka/PycharmProjects/Nb/assignment2/hw2_train/train/ham", "spam","C:/Users/tejamukka/PycharmProjects/Nb/assignment2/new_data/CSDMC2010_SPAM/CSDMC2010_SPAM/TESTING")


  for file in dirham:
      spamTestCount+= 1
      spamFilesPath = pathhame  +'/'+file
      f = open(spamFilesPath,'r')
      sectionSpamTest = f.read()
      #tokens = parseText(sectionSpamTest)
      tokens = Test(sectionSpamTest)
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
               #hamscore+= 0
         # print hamscore,tokenkey
          #spamscore+= log(spamcondprob[tokenkey])
      for tokenkey in tokens:
          if spamcondprob.has_key(tokenkey):
            spamscore += log(spamcondprob[tokenkey],10)
          else:
            spamscore += log(spamnoshowprob,10)
            #spamscore +=0
        #  print spamscore,tokenkey
      if hamscore <= spamscore:
          spamsuccesscount+=1
      else:
          spamfailurecount+=1
  #print spamsuccesscount,"looking for spam accuracy"
  #print spamfailurecount,"looking for spam failure"
  #print spamsuccesscount/(spamfailurecount + spamsuccesscount), "spam_accuracy"
      #print hamscore,spamscore,"thisoe"
      #print sectionHamTest

  #  hamTestCount,sectionHamTest
  return spamTestCount

note = spamSectionTest("","")
#list = parseText(note[1])
#print list
#def testMultinomialNB():

print spamsuccesscount,spamfailurecount, hamsuccesscount, hamfailurecount

print (hamsuccesscount+spamsuccesscount)/(hamsuccesscount+spamsuccesscount+hamfailurecount+ spamfailurecount) ,"final accuracy for NB without stop words"