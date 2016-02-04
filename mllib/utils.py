# Common utils used in machine learning algorithms

import math
from collections import defaultdict

def entropy(data, target_attr):
  # assuming data is collection of lists
  # [0 1 0 1 0 1 1 0]
  # target_attr: is index of the class attribute

  val_freq= {}
  data_entropy = 0.0

  # calculate the frequency of each of the values in the target attr
  #print "length of data ",len(data)
  for record in data:
    if record[target_attr]:
      if(val_freq.has_key(record[target_attr])):
        val_freq[record[target_attr]] += 1.0
      else:
        val_freq[record[target_attr]] = 1.0

    # Calculate the entropy of the data for the target attribute
  for freq in val_freq.values():
    data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2)

  return data_entropy


def variance_impurity(data , target_attr):
    val_freq= {}
    data_entropy = 0.0

    # calculate the frequency of each of the values in the target attr
    #print "length of data ",len(data)
    for record in data:
      if(val_freq.has_key(record[target_attr])):
        val_freq[record[target_attr]] += 1.0
      else:
        val_freq[record[target_attr]] = 1.0

      # Calculate the entropy of the data for the target attribute
    for freq in val_freq.values():
      data_entropy *= freq/sum(val_freq.values())

    return data_entropy

def information_gain(data, attr, target_attr, fitness_func):
  """
    Information gain measures the decrease in entropy that results from splitting a set of instances based on an attribute.

    I(T,X) =  Entropy(T) - Entropy(T,X)

    If X has multiple values then we compute expected entropy from value X.
  """
  val_freq = {}
  subset_entropy = 0.0

  # calculate the frequency of each of the values in the target attribute
  for record in data:
    if(val_freq.has_key(record[attr])):
      val_freq[record[attr]] += 1.0
    else:
      val_freq[record[attr]] = 1.0

  # calculate the sum of entropy for each subset of records weighted
  # by their probability of occurence
  for val in val_freq.keys():
    val_prob = val_freq[val] / sum(val_freq.values())
    data_subset = [ record for record in data if record[attr] == val]
    subset_entropy += val_prob* fitness_func(data_subset, target_attr)

  # subtract the entropy of the chosen attribute from the entropy of the whole data set
  return (entropy(data, target_attr) - subset_entropy)

def majority_value(data, class_attr):
  """
    Creates a list of all values in the target attribute for each record in the data list object,
    and returns the value that appears in the list the most frequently.
  """
  val_freq = {}
  for record in data:
      if val_freq.has_key(record[class_attr]):
          val_freq[class_attr] += 1.0
      else:
          val_freq[class_attr] = 1.0

  max_freq = 0
  max_key = None
  for key, value in val_freq.iteritems():
      if max_freq < value:
        max_freq = value
        max_key = key

  return max_key

def get_examples(data, attr, val):
    '''
        Returns dataset where attr value is val
    '''
    return [record for record in data if record[attr] == val]

def split_instances(instances, attribute_index):
    '''
        Returns a list of dictionaries, splitting a list of instances according to
        their values of a specificied attribute index

        The key of each dictionary is a distinct value of attribute_index, and the value
        of each dictionary is a list representing the subset of instances that have value
        for the attribute
    '''
    partitions = defaultdict(list)
    for instance in instances:
        partitions[instance[attribute_index]].append(instance)
    return partitions

def get_values(data, attr):
    '''
        it returns the list of attribute values present in dataset
    '''
    s = set()
    for record in data:
        s.update([record[attr],])
    return s
