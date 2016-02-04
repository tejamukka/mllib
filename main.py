#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mllib.decisionTree import DecisionTree
import sys
import re

def train(training_set, option):
    data = []
    with open(training_set,'r') as f:
        for line in f:
            data.append(re.split(',| |\n',line)[:-1])

    attributes = data[0]
    target_attr = attributes[-1]

    print "attributes : ", attributes
    print "target attribute ", target_attr

    # Decision Tree algorithm starts here
    dt = DecisionTree(option)
    dt.fit(data[1:], attributes, target_attr )
    return dt
    #print "\n examples accuracy : ", ( dt.validate( data[1:], target_attr) )

def accuracy(decistiontree, testfilename):
    data = []
    with open(testfilename, 'r') as f:
        for line in f:
            data.append(re.split(',| |\n',line)[:-1])

    attributes = data[0]
    target_attr = attributes[-1]

    pcnt, ncnt = decistiontree.validate(data[1:], target_attr)

    print "\n--------------------------------------------------\n"
    print "TESTING RESULTS on %s" %(testfilename)
    print "POSITIVE : ", pcnt
    print "NEGATIVE : ", ncnt
    print "Accuracy ", pcnt*1.0/(pcnt+ncnt)
    print "---------------------------------------------------"

def print_stats(dt, to_print, validation_set, test_set):
    if to_print == "yes":
        dt.stats()
    accuracy(dt, validation_set)
    accuracy(dt, test_set)

def main():
    if len(sys.argv) != 7:
        print('''
Invalid input arguments.
Please specify input as :
python main.py <L> <K> <training_set> <validation_set> <test_set> <to_print>
''')
        sys.exit(1)

    # read inputs from command line

    val_l = sys.argv[1]
    val_k = sys.argv[2]
    train_set = sys.argv[3]
    validation_set = sys.argv[4]
    test_set = sys.argv[5]
    to_print = sys.argv[6]

    # train the decisionTree over the training data
    dt1 = train(train_set, DecisionTree.ENTROPY)
    print_stats(dt1, to_print, validation_set, test_set)

    dt2 = train(train_set, DecisionTree.VARIANCE_IMPURITY)
    print_stats(dt2, to_print, validation_set, test_set)


if __name__ == '__main__':
    main()
