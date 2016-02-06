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

    #print "attributes : ", attributes
    #print "target attribute ", target_attr

    # Decision Tree algorithm starts here
    dt = DecisionTree(option)
    dt.fit(data[1:], attributes, target_attr )
    return dt
    #print "\n examples accuracy : ", ( dt.validate( data[1:], target_attr) )

def print_stats(dt, to_print, validation_set, test_set):
    if to_print == "yes":
        dt.stats()
    #dt.accuracy(validation_set)
    dt.accuracy(test_set)

def main():
    if len(sys.argv) != 7:
        print('''
Invalid input arguments.
Please specify input as :
python main.py <L> <K> <training_set> <validation_set> <test_set> <to_print>
''')
        sys.exit(1)

    # read inputs from command line

    val_l = int(sys.argv[1])
    val_k = int(sys.argv[2])
    train_set = sys.argv[3]
    validation_set = sys.argv[4]
    test_set = sys.argv[5]
    to_print = sys.argv[6]

    # train the decisionTree over the training data
    print "informaiton gain decision tree"
    dt1 = train(train_set, DecisionTree.ENTROPY)
    dt1.accuracy(test_set)

    print "AFTER PRUNING"
    dt1.prune(validation_set, val_l, val_k)
    dt1.accuracy(test_set)


    print "variance impurity decision tree"
    dt2 = train(train_set, DecisionTree.VARIANCE_IMPURITY)
    dt2.accuracy(test_set)

    print "AFTER PRUNING"
    dt2.prune(validation_set, val_l, val_k)
    dt2.accuracy(test_set)

    if to_print == "yes":
        print "\n Decision tree information gain "
        dt1.stats()

        print "\n Decision tree variance impurity "
        dt2.stats()


if __name__ == '__main__':
    main()
