# Common utils used in machine learning algorithms

import math
from collections import defaultdict

def fetch_values(dataset, attr):
    
    #  This method returns the list of attributes values present in the dataset
    
    set = set()
    for record in dataset:
        set.update([record[attr],])
    return set
 


def most_freq_attr_val(data, class_attr):
 
    #This is used to return the most frequently repeated values in the possibles values of the given class_attr
  
  value_freq = {}
  for datarow in data:
      if value_freq.has_key(datarow[class_attr]):
          value_freq[datarow[class_attr]] += 1.0
      else:
          value_freq[datarow[class_attr]] = 1.0

  max_freq_value = 0
  max_attr_val = None
  for key, value in value_freq.iteritems(): # Iterates and find the most frequently attribute value 
      if max_freq_value < value:
        max_freq_value = value
        max_attr_val = key

  return max_attr_val


def getAttribute_With_GivenValue(dataset, attribute, val):
    
    #    This method returns the given dataset  where attribute  value is val
    
    return [row for row in dataset if row[attribute] == val]
