#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Implementation of Decision Tree
from mllib.utils import *
import collections
import Queue
import random

class DecisionTree:

  _tree = {}      # It stores tree as dictionary
  _attribute_names =[]

  # algorithms to choose next attribute
  ENTROPY = 1
  VARIANCE_IMPURITY = 2

  def __init__(self, option=2):
      if option == self.ENTROPY:
        self.fitness_func = entropy

      elif option == self.VARIANCE_IMPURITY:
        self.fitness_func = variance_impurity

  def walk(self, dct, depth):
      if isinstance(dct, dict):
          node = dct.keys()[0]
          for key, value in dct[node].iteritems():
              print '\n' + '|'*depth,
              print "%s = %s : " %(node, key),
              self.walk(value, depth+1)
      else:
          print dct,
  def stats(self):
      self.walk(self._tree, 0)

  def fit(self, data, attributes, target_attr):
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

  def choose_attribute(self, data, attributes, class_attr, fitness):
      '''
        Cycles through all the attributes and returns the attribute with the highest
        informaiton gain
      '''
      best = (-1e999999, None)
      #print attributes
      for attr in attributes:
          if attr == class_attr:
              continue
          gain = information_gain(data, attr, class_attr, fitness)
          #print (gain, attr)
          best = max(best, (gain, attr))
      return best[1]

  def walk_validate(self,dct, record, depth = 0):
      if isinstance(dct,dict):
          node = dct.keys()[0]
          ind = self._attribute_names.index(node)
          for key, val in dct[node].iteritems():
              if( key == record[ind]):         # if value matches with record
                return self.walk_validate(val, record, depth+1)
      return dct

  def get_rules():
      '''
        get all the rules as path from root to leaves.
      '''

  def prune(self, dataset, iterations, high):
      '''
        Post pruning step for decision trees. It prunes / deletes nodes to decrease accuracy on
        training set but increase accuracy on validation set.
      '''
      for i in range(iterations):
          m = random.randomInt(1, high)
          for i in range(m):


  def validate(self,test_set, target_attr):
      '''
        It simply checks decision tree accuracy against test data set.
      '''
      ncnt = 0
      pcnt = 0
      index = self._attribute_names.index(target_attr)
      for record in test_set:
          if( self.walk_validate(self._tree, record) == record[index]):
             pcnt+=1
          else:
             ncnt+=1
      return (pcnt, ncnt)

  def _create_tree(self, data, attributes, target_attr, fitness_func):
    """
      Returns a new decision tree based on the examples given
    """
    data = data[:]
    vals = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)

    # if the dataset is empty or attributes list is empty, return the default value
    if not data or (len(attributes) - 1) < 0:
        return default

    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # choose the next best attribute to best classify our data
        best = self.choose_attribute(data, attributes, target_attr, fitness_func)

        # create a new node
        tree = {self._attribute_names[best]:{}}

        # create a new decision tree / sub-node for each of the values in the best attribute field
        for val in get_values(data, best):
            subtree = self._create_tree(get_examples(data, best, val),
                    [ attr for attr in attributes if attr != best],
                    target_attr,
                    fitness_func )

            # Add the new subtree to empty dictionary object in our new tree/node we just created
            tree[self._attribute_names[best]][val] = subtree
    return tree
