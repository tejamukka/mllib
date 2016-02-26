#!/usr/bin/env python

# Naive Bayes Implementation
from mllib.utils import *
import csv
from mllib.naive_bayes.Pool import Pool
import os

correctCount = 0
wrongCount = 0
labels = ["spam", "ham"]

base_dir = "data/train/"
p = Pool()
for label in labels:
    p.learn(base_dir + label, label)

base_dir = "data/test/"
stop_words = "data/stopwords_en.txt"
p.read_stop_words(stop_words)

def log_accuracy(correctLabel, foundLabel):
    global correctCount, wrongCount
    if(correctLabel == foundLabel):
        correctCount += 1
    else:
        wrongCount += 1

def report(correctCount, wrongCount):
    print("Total Cases tested : %d"%(correctCount + wrongCount))
    print("Correct cases", correctCount)
    print("Wrong cases ", wrongCount)
    print("Accuracy: ", correctCount*1.0/ (correctCount + wrongCount)*1.0)

for label in labels:
    if os.path.isdir(base_dir + label):
        dir = os.listdir(base_dir + label)
        for file in dir:
            res = p.probability(base_dir + label + "/" + file)
            log_accuracy(label, res[0][0])
            print( label + ": " + file + ": " + str(res))
report(correctCount, wrongCount)
