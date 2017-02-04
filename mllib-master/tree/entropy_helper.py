#Utilies used for calculating and using the entropy helper functions

import math
from collections import defaultdict

def classEntropy(dataset, attr): #Calculates the class level entropy of the given dataset
  classEntropyValue = 0.0
  levelCount = {}
  datarows = len(dataset)
  for datarow in dataset: # Traverse all the rows
	currentLevel = datarow[-1]
	if levelCount.has_key(currentLevel):
		levelCount[currentLevel]+=1.0
	else:	
		levelCount[currentLevel] =1.0
  for freq in levelCount.values():
  # change datarows to len(data) to make it work 
	classEntropyValue+= (-freq/datarows) * math.log((freq/datarows),2)
  return classEntropyValue	


def class_variance_impurity(dataset , attr):
  levelCount = {}
  
  impurity = 1.0
  for datarow in dataset: # traversing through the whole dataset :row by row
	currentLevel = datarow[-1]   # Checking for the last column of the given data and in this case it is the class variable.
	if levelCount.has_key(currentLevel): # Checks if the key is present and increments the count if its present.
		levelCount[currentLevel]+=1.0
	else:	
		levelCount[currentLevel] =1.0  # If its not present , it creates a new key 
  classVarianceEntropyValue = -1.0  
  for freq in levelCount.values():  # taking the count for each class_value and multiplying the probabilities
    classVarianceEntropyValue *= freq/len(dataset) # Implemented the class Entropy as described.

  return classVarianceEntropyValue

def information_gain(data, attr, target_attribute, fitness_func):
  
  # This gives the decrease in entropy because of the splitting the set with respect to an attribute
  value_frequency = {}
  subset_entropy = 0.0

  # Gives the frequency of each possible value in the target attribute
  for record in data:
    if(value_frequency.has_key(record[attr])): 
	# increments the value if the key is already present
      value_frequency[record[attr]] += 1.0
    else:
      value_frequency[record[attr]] = 1.0   # Creates the corresponding key if it is not present

  # Evaluate the entropy sums for each subsets present weighted by their probabilities of occurence
  # code
  for val in value_frequency.keys():   # for each value in keys, traverse and get the corresponding probabilities
    val_prob = value_frequency[val] / sum(value_frequency.values())
    data_subset = [ record for record in data if record[attr] == val]  # Retrieve the dataset subset excluding that attr
    subset_entropy += val_prob* fitness_func(data_subset, target_attribute) # recursive calculating of subset_entropy

  # subtract the entropy of the chosen attribute from the entropy of the whole data set
  return (fitness_func(data, target_attribute) - subset_entropy)

def minimum_value(dataset, class_attr):#Calculates the miniority values for the given class
  value_frequency ={}
  for datarow in dataset:
	  if value_frequency.has_key(datarow[class_attr]):	# Same logic of incrementing if exists else create new one
			value_frequency[datarow[class_attr]] +=1.0
	  else:		
            value_frequency[datarow[class_attr]] =1.0
  min_freq =1000000  # putting it to some higher value
  min_key = None 
  for key, value in value_frequency.iteritems():
	  if min_freq > value:	
			min_freq = value  # finding and updating the min_freq value
			min_key =key
  return min_key  # return the min_key 


def fetch_values(data, attr):
    s = set()
    for record in data:
        s.update([record[attr],]) # Fetches the values corresponding to the given attr
    return s
	
def maximum_value(dataset, class_attr):
# Calculates the majority values for the given class  
  value_frequency = {}
  for record in dataset:
      if value_frequency.has_key(record[class_attr]):
          value_frequency[record[class_attr]] += 1.0# Same logic of incrementing if exists else create new one
      else:
          value_frequency[record[class_attr]] = 1.0 # Create new one 

  max_freq = 0
  max_key = None
  for key, value in value_frequency.iteritems():
      if max_freq < value:
        max_freq = value  # finding and updating the min_freq value
        max_key = key

  return max_key
