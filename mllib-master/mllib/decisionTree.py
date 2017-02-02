#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Implementation of Decision Tree
from mllib.attr_helper import *
from mllib.entropy_helper import *
import collections
import Queue
import random
import copy
import re

class Node(object):

    def __init__(self, name, majority_class):
        self._name = name
        self._majority_class = majority_class

    def getName(self):
        return self._name

    def getClass(self):
        return self._majority_class

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

class DecisionTree:

  # algorithms to choose next attribute
  ENTROPY = 1
  VARIANCE_IMPURITY = 2

  def __init__(self, option=2):
      self._tree = {}
      self._attribute_names = []
      self._inner_nodes = []

      if option == self.ENTROPY:
        self.fitness_func = classEntropy

      elif option == self.VARIANCE_IMPURITY:
        self.fitness_func = class_variance_impurity

  def replace_node(self, dct, tofind):
      if isinstance(dct, dict):
          node = dct.keys()[0]
          print "comparing ", tofind, "   ", node
          if  tofind.getName() == node.getName():
              dct[node]= node.getClass()
              return 1
          print "dct ", dct
          try:
              for key, value in dct[node].iteritems():
                  ret = self.replace_node(value, tofind)
                  if ret == 1:
                      return ret
          except:
              # dct[node] is a string
              return 0
      return 0

  def _create_tree(self, dataset, attributes, target_attr, fitness_func):
    """
      Returns a new decision tree based on the examples given
    """
    dataset = dataset[:]
    vals = [datarow[target_attr] for datarow in dataset]
    default = most_freq_attr_val(dataset, target_attr)

    # if the dataset is empty or attributes list is empty, return the default value
    if not dataset or (len(attributes) - 1) <= 0:
        return default

    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # choose the next best attribute to best classify our data
        best = self.choose_best_attribute(dataset, attributes, target_attr, fitness_func)

        # create a new node
        #print "best attribute ",best
        node = Node(self._attribute_names[best], default)
        tree = {node:{}}

        # insert newly created node
        self._inner_nodes.append(tree)

        # create a new decision tree / sub-node for each of the values in the best attribute field
        for val in get_values(dataset, best):
            subsetTree = self._create_tree(getAttribute_With_GivenValue(dataset, best, val),
                    [ attr for attr in attributes if attr != best],
                    target_attr,
                    fitness_func )

            # Add the new subtree to empty dictionary object in our new tree/node we just created
            tree[node][val] = subsetTree

    return tree
	
  def walk(self, dct, depth):
      if isinstance(dct, dict):
          node = dct.keys()[0]
          try:
              for key, value in dct[node].iteritems():
                  print '\n' + '|'*depth,
                  print "%s = %s : " %(node, key),
                  self.walk(value, depth+1)
          except:
              print dct[node],
      else:
          print dct,
		  
  def print_tree(self):
      self.walk(self._tree, 0)

  def fit(self, data, attributes, target_attr):
      '''
        Public method to fit data into a decision tree.
      '''
      self._attribute_names = attributes
      # convert attributes to integer array
      attr_list = [ i for i in range(len(attributes))]
      try:
          index = attributes.index(target_attr)
      except ValueError:
          print(" No class attribute found. Can't build the tree.")

      # Selecting fitness function to choose attribute
      self._tree = self._create_tree(data, attr_list, index, self.fitness_func)
      #print self._tree

  def choose_best_attribute(self, data, attributes, class_attr, fitness):
      '''
        Cycles through all the attributes and returns the attribute with the highest
        informaiton gain
      '''
      # checking purppose
      # pick attribute randomly
      best = (-1e999999, None)
      #print attributes
      for attr in attributes:
          if attr == class_attr:
              continue
          gain = information_gain(data, attr, class_attr, fitness)
          #print (gain, self._attribute_names[attr])
          best = max(best, (gain, attr))
      return best[1]

  def walk_validate(self,dct, record, depth = 0):
      if isinstance(dct,dict):
          node = dct.keys()[0]
          ind = self._attribute_names.index(node.getName())
          try:
              for key, val in dct[node].iteritems():
                  if( key == record[ind]):         # if value matches with record
                    return self.walk_validate(val, record, depth+1)
          except:
              return dct[node]
      return dct


  def prune(self, dataset, iterations, high):
      '''
        Post pruning step for decision trees. It prunes / deletes nodes to decrease accuracy on
        training set but increase accuracy on validation set.
      '''
      opcnt, oncnt = self.printAccuracy(dataset,0)
      bestree = copy.deepcopy(self._tree)
      for i in range(iterations):
          m = random.randint(1, high)
          for i in range(m):
            # restore self._tree
            #self._tree = copy.deepcopy(original_tree)
            #print "tree before ",self._tree
            # pick any node and drop it. Check the performance against validation set
            n = len(self._inner_nodes) -1
            if n> 0:
                P = random.randint(0,n-1)
            else:
                P = 0
            # pick the node

            node = self._inner_nodes[P].keys()[0]
            #print "node ",node

            temp = self._inner_nodes[P][node]
            self._inner_nodes[P][node] = node.getClass()
            #print "find ", self.replace_node(tree, self._inner_nodes[P].keys()[0])
            #print "tree after ", self._tree

            # get the accuracy
            pcnt, ncnt = self.printAccuracy(dataset,0)
            #print "new accuracy ", pcnt*1.0/(pcnt + ncnt)
            if pcnt*1.0/(pcnt + ncnt) > opcnt*1.0 / (opcnt + oncnt):
                #print "new improvement ", pcnt*1.0/(pcnt + ncnt)
                opncnt = pcnt
                oncnt = ncnt
                bestree = copy.deepcopy(self._tree)
            # restore the tree
            self._inner_nodes[P][node] = temp

      self._tree = bestree

  def validate(self,test_set, target_attr):
      '''
        It simply checks decision tree accuracy against test data set.
      '''
      negcount = 0
      poscount = 0
      index = self._attribute_names.index(target_attr)
      for datarow in test_set:
          if( self.walk_validate(self._tree, datarow) == datarow[index]):
             poscount+=1
          else:
             negcount+=1
      return (poscount, negcount)

  def printAccuracy(self, testfilename, toprint=1):
      dataset = []
      with open(testfilename, 'r') as f:
          for line in f:
              dataset.append(re.split(',| |\n',line)[:-1])

      attributes = dataset[0]
      target_attr = attributes[-1]

      poscount, negcount = self.validate(dataset[1:], target_attr)
      if toprint:
          print "\n--------------------------------------------------\n"
          print "TESTING RESULTS on test dataset:%s" %(testfilename)
          print "POSITIVE CLASS : ", poscount
          print "NEGATIVE CLASS: ", negcount
          print "OverAll Accuracy: ", poscount*1.0/(poscount+negcount)
          print "---------------------------------------------------"
      return (poscount, negcount)

  