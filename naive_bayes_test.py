#!/usr/bin/env python

# Naive Bayes Implementation
from mllib.utils import *
import csv
from mllib.naive_bayes.Pool import Pool
import os, sys



def report(correctCount, wrongCount):
    print("Total Cases tested : %d"%(correctCount + wrongCount))
    print("Correct cases", correctCount)
    print("Wrong cases ", wrongCount)
    print("Accuracy: ", correctCount*1.0/ (correctCount + wrongCount)*1.0)


def naive_bayes():
    correctCount = 0
    wrongCount = 0

    for label in labels:
        if os.path.isdir(base_dir + label):
            dir = os.listdir(base_dir + label)
            for file in dir:
                res = p.probability(base_dir + label + "/" + file)
                if label == res[0][0]:
                    correctCount += 1
                else:
                    wrongCount += 1
                #print( label + ": " + file + ": " + str(res))
    return (correctCount, wrongCount)

def logistics_regression():
    correctCount = 0
    wrongCount = 0
    p.train(labels[0])
    for label in labels:
        if os.path.isdir(base_dir + label):
            dir = os.listdir(base_dir + label)
            for file in dir:
                res = p.regression(base_dir + label + "/" + file, labels[0], labels[1])
                if label == res[0][0]:
                    correctCount += 1
                else:
                    wrongCount += 1
                #print( label + ": " + file + ": " + str(res))

    return (correctCount, wrongCount)

if __name__ == '__main__':
    labels = ["spam", "ham"]

    base_dir = "data/train/"
    p = Pool()
    for label in labels:
        p.learn(base_dir + label, label)

    base_dir = "data/test/"
    stop_words = "data/stopwords_en.txt"
    p.read_stop_words(stop_words)

    #(correctCount, wrongCount) = naive_bayes()
    #report(correctCount, wrongCount)

    (correctCount, wrongCount) = logistics_regression()
    report(correctCount, wrongCount)
