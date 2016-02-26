#!/usr/bin/env python

from mllib.naive_bayes.BagOfWords import BagOfWords
from mllib.naive_bayes.Document import Document

# Naive Bayes Category class
class Category(Document):

    def __init__(self):
        self._vocabulary = BagOfWords()
        Document.__init__(self)
        self._number_of_docs = 0

    def probability(self, word):
        """ returns the probability of word given the class self """
        voc_len = len(Document._vocabulary.len())
        sumN = 0
        for word in Document._vocabulary.Words():
            sumN += Category._vocabulary.word_freq(word)
        N = self.word_freq(word)
        erg = 1 + N
        erg /= (voc_len + sumN)

        return erg

    def __add__(self, other):
        """ Overloading the '+' operator. Adding two categories"""
        res = Category(self._vocabulary)
        res._vocabulary = self._vocabulary + other._vocabulary

        return res

    def SetNumberOfDocs(self, number):
        self._number_of_docs = number

    def NumberOfDocuments(self):
        return self._number_of_docs
