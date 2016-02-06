=====
mllib
=====
Machine Learning in Python

Description
===========

It contains machine learning algorithms taught in CS7301 [ Advanced Machine Learning ] course at UTD.

Test
====
Simply run below command for testing machine library functionality.

> python main.py <K> <L> <training_set> <validation_set> <test_set> <to_print>

for example:
> python main.py 1 2 data/training_set.csv  data/validation_set.csv data/test_set.csv yes

It will run decision tree classifier on training set and report back the accuracy of 

1) Information Gain heuristics (  Before & After pruning )
2) Variance Impurity heuristics ( Before & After pruning )

to_print will make program to print the tree on console. Sample output is attached as sample_output.txt
