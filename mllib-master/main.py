# Reading the arguments from the cmd and decides whether to print the tree or not and also the paths to the various datasets
 

from tree.decisionTree import OptimalDecisionTree
import sys
import re

def train(training_set, option): # Training using the training set and option is used to decode the heuristic
    data = []
    with open(training_set,'r') as f: # Open the files training set 
        for line in f:
            data.append(re.split(',| |\n',line)[:-1]) # Split with either the new line or , and append all those values 

    attributes = data[0]      # Take the first row
    target_attr = attributes[-1] ## Selecting the class required.

    # Decision Tree algorithm starts here
    decisiontree = OptimalDecisionTree(option)
    decisiontree.fit(data[1:], attributes, target_attr )  # Fit the decision tree using the given attributes
    return decisiontree

def print_stats(decisiontree, to_print, validation_set, test_set): # This prints the stats for the given decision tree
    if to_print == "yes": # Looks for the command from the cmd line and prints only if it is yes
        decisiontree.stats() # gives the stats of the corresponding decision tree
    decisiontree.accuracy(test_set)

def main():
    if len(sys.argv) != 7:
        print('''
These are not valid input arguments.
Please re-enter input as :
python main.py <L> <K> <training_set> <validation_set> <test_set> <to_print>
''')
        sys.exit(1)

    # reads the arguments  from command line and treats them as the inputs

    value_l = int(sys.argv[1])
    value_k = int(sys.argv[2])
    training_set = sys.argv[3] # Selects the training set 
    validation_set = sys.argv[4]
    test_set = sys.argv[5]
    print_tree = sys.argv[6] # decides whether to print 

    # training  the give decision Tree in the training data
    print "Statistics of decision tree using information gain to calculate entropy"
    decisiontree1 = train(training_set, OptimalDecisionTree.CLASS_ENTROPY)
    decisiontree1.printAccuracy(test_set)
    #Pruning and trying to improve the accuracy of the given decision tree
    print "Statistics AFTER PRUNING of decision tree using information gain to calculate entropy"
    decisiontree1.prune(validation_set, value_l, value_k)
    decisiontree1.printAccuracy(test_set)

	# This one uses the second heuristic to build the decision tree 
    print "Statistics of decision tree using variance impurity to calculate entropy"
    decisiontree2 = train(training_set, OptimalDecisionTree.VARIANCE_IMPURITY)
    decisiontree2.printAccuracy(test_set)
    # This one prunes the second tree and improves the accuracy 
    print "Statistics AFTER PRUNING of decision tree using variance impurity to calculate entropy"
    decisiontree2.prune(validation_set, value_l, value_k)
    decisiontree2.printAccuracy(test_set)

    if print_tree == "yes":
        print "\n Printing the Decision tree using information gain "
        decisiontree1.print_tree() # Printing the first decision tree

        print "\n Printing the Decision tree using variance impurity "
        decisiontree2.print_tree() # Printing tthe second decision tree 


if __name__ == '__main__':
    main()
