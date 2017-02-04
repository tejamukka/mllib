

# Implementation of Decision Tree
from tree.attr_helper import *
from tree.entropy_helper import *
import random
import collections
import re
import copy
import Queue

class Node(object):# creates a node 

    def __init__(self, nodename, majority_class):
        self._name = nodename
        self._majority_class = majority_class

    def getNodeName(self):
        return self._name

    def getMajorityClass(self):  # returns the majority_class of the tree 
        return self._majority_class

    def __str__(self):
        return self._name # returns the str of the name 
	### self.name 
    def __repr__(self):
        return self._name

class OptimalDecisionTree:

  # The two heuristics to choose the choose next attribute to split on 
  VARIANCE_IMPURITY = 2
  CLASS_ENTROPY = 1
  

  def __init__(self, option=2):
      self._tree = {}
      self._attribute_names = []
      self._inner_nodes = []

      if option == self.CLASS_ENTROPY:
        self.fitness_func = classEntropy

      elif option == self.VARIANCE_IMPURITY:
        self.fitness_func = class_variance_impurity
	
  def _create_tree(self, dataset, attributes, target_attr, fitness_func):
    #Creates a new tree based on the given training data set 
    dataset = dataset[:]
    vals = [datarow[target_attr] for datarow in dataset]
    default = most_freq_attr_val(dataset, target_attr)

    # This checks if the data value is not present and returns the default value.
    if not dataset or (len(attributes) - 1) <= 0:
        return default

    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # choose the next best attribute to best classify our data
        best = self.choose_best_attribute(dataset, attributes, target_attr, fitness_func)

        # create a new node
        #print the found "best attribute ",best
        node = Node(self._attribute_names[best], default)
        tree = {node:{}}

        # The newly created node is to be inserted.
        self._inner_nodes.append(tree)

        # create a new decision tree / sub-node for each of the values in the best attribute field
        for val in fetch_values(dataset, best):
            subsetTree = self._create_tree(getAttribute_With_GivenValue(dataset, best, val),
                    [ attr for attr in attributes if attr != best],
                    target_attr,
                    fitness_func )

            # Add the new subtree to empty dictionary object in our new tree/node we just created
            tree[node][val] = subsetTree

    return tree
	
  def walk(self, dct, treedepth): # traversing through the tree and print the tree 
      if isinstance(dct, dict):
          node = dct.keys()[0] # gets all the possible key values 
          try:
              for key, value in dct[node].iteritems():
                  print '\n' + '|'*treedepth, # printing a new lines and the space as required.
                  print "%s = %s : " %(node, key),
                  self.walk(value, treedepth+1)  
          except:
              print dct[node],
      else:
          print dct,
		  
  def print_tree(self):
      self.walk(self._tree, 0)

  def fit(self, data, attributes, target_attr):
      # This is the method which is used to fit the dataset
      self._attribute_names = attributes
      # convert attributes to integer array
      attr_list = [ i for i in range(len(attributes))] # gets the list of the attributes in the dataset
      try:
          index = attributes.index(target_attr)
      except ValueError:
          print(" No class attribute found. Can't build the tree.")

      # Selecting fitness function to choose attribute
      self._tree = self._create_tree(data, attr_list, index, self.fitness_func)
      #print self._tree

  def choose_best_attribute(self, data, attributes, class_attr, fitness):
      #chooses the best attribute with the highest information_gain
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
      if isinstance(dct,dict): # Checks if its the correct instance
          node = dct.keys()[0]
          ind = self._attribute_names.index(node.getNodeName())
          try:
              for key, val in dct[node].iteritems(): # Traverse through all the nodes in dct
                  if( key == record[ind]):         # if value matches with record
                    return self.walk_validate(val, record, depth+1)
          except:
              return dct[node]
      return dct


  def prune(self, dataset, iterations, high):
      
        # This method implements the pruning process for decision trees. This prunes and tried to improve the accuracy in the validation 
		#set data even though it might decrease the accuracy on the training data set.
        
      
      oldpcnt, oldncnt = self.printAccuracy(dataset,0)
      bestree = copy.deepcopy(self._tree) # copies the tree before pruned
      for i in range(iterations):
          m = random.randint(1, high) # selects a random number in th given range 
          for i in range(m):
            # Pick any random node and drop the node.
           
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
            self._inner_nodes[P][node] = node.getMajorityClass()
            
            # This gets the accuracy on the given dataset
            pcnt, ncnt = self.printAccuracy(dataset,0)
            #prints the new accuracy 
            if pcnt*1.0/(pcnt + ncnt) > oldpcnt*1.0 / (oldpcnt + oldncnt):
                #print "new improvement ", pcnt*1.0/(pcnt + ncnt)
                opncnt = pcnt
                oldncnt = ncnt
                bestree = copy.deepcopy(self._tree) # copies the improved tree back 
            # restore the tree
            self._inner_nodes[P][node] = temp

      self._tree = bestree

  def validate(self,test_set, target_attr):
      #This checks the accuracy of the given data set against the training model built from training data 
      negcount = 0
      poscount = 0
      index = self._attribute_names.index(target_attr)
      for datarow in test_set: # traverse each row
          if( self.walk_validate(self._tree, datarow) == datarow[index]):
             poscount+=1 # Increase the positive count 
          else:
             negcount+=1
      return (poscount, negcount)

  def printAccuracy(self, filename, toprint=1): # This method prints the accuracy of both the heuristics
      dataset = []
      with open(filename, 'r') as f: # Opens the file 
          for line in f:
              dataset.append(re.split(',| |\n',line)[:-1]) # appends the data 

      data_attributes = dataset[0]
      target_attr = data_attributes[-1]

      poscount, negcount = self.validate(dataset[1:], target_attr)
      if toprint:
          print "\n--------------------------------------------------\n"
          print "TESTING RESULTS on test dataset:%s" %(filename) 
          print "POSITIVE CLASS : ", poscount # positive result count 
          print "NEGATIVE CLASS: ", negcount   ## negative result count 
          print "OverAll Accuracy: ", poscount*1.0/(poscount+negcount)
          print "---------------------------------------------------"
      return (poscount, negcount)

  