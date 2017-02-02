# Common utils used in machine learning algorithms

import math
from collections import defaultdict

def get_values(dataset, attr):
    '''
        it returns the list of attribute values present in dataset
    '''
    set = set()
    for record in dataset:
        set.update([record[attr],])
    return set
 

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

def most_freq_attr_val(data, class_attr):
  """
    Creates a list of all values in the target attribute for each record in the data list object,
    and returns the value that appears in the list the most frequently.
  """
  value_freq = {}
  for datarow in data:
      if value_freq.has_key(datarow[class_attr]):
          value_freq[datarow[class_attr]] += 1.0
      else:
          value_freq[datarow[class_attr]] = 1.0

  max_freq_value = 0
  max_attr_val = None
  for key, value in value_freq.iteritems():
      if max_freq_value < value:
        max_freq_value = value
        max_attr_val = key

  return max_attr_val


def getAttribute_With_GivenValue(dataset, attr, val):
    '''
        Returns dataset where attr value is val
    '''
    return [row for row in dataset if row[attr] == val]
