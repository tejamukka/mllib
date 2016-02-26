from mllib.naive_bayes.BagOfWords import BagOfWords
from mllib.naive_bayes.Category import Category
from mllib.naive_bayes.Document import Document

import os
import math
import re

class Pool(object):
    def __init__(self):
        self.__document_classes = {}
        self._vocabulary = BagOfWords()
        self.__no_of_documents = 0
        self._stop_words = None


    def read_stop_words(self, filename):
        with open(filename,"r") as f:
            text = f.read()
            self._stop_words = re.split("(?:(?:[^a-zA-Z]+')|(?:'[^a-zA-Z]+))|(?:[^a-zA-Z']+)",text)[:-1]

    def learn(self, directory, dclass_name):
        """ Learn from files in directory """
        x = Category()
        dir = os.listdir(directory)

        for file in dir:
            d = Document()
            print(directory + " / "+ file)
            d.read_document(directory +"/"+ file, self._stop_words)
            x._vocabulary = x._vocabulary + d._vocabulary
            self.__no_of_documents += 1

        self.__document_classes[dclass_name] = x
        self._vocabulary = self._vocabulary + x._vocabulary

        #print(self.__document_classes[dclass_name]._vocabulary.BagOfWords())
        x.SetNumberOfDocs(len(dir))


    def probability(self, doc, dclass = ""):

        if dclass:
            #print(self._vocabulary.BagOfWords())
            #print("Document vocabulary ", dclass)
            #print(self.__document_classes[dclass].BagOfWords())
            doclength = self.sum_words_in_class(dclass)

            d = Document()
            d.read_document(doc, self._stop_words)
            prod = 1
            for i in d.Words():
                wf = 1 + self.__document_classes[dclass].words_freq(i)
                l = len(self._vocabulary)
                r = wf/(doclength + l)
                prod += (d.words_freq(i))*math.log(r)

            prob = prod + math.log(self.__document_classes[dclass].NumberOfDocuments() / self.__no_of_documents)

            return prob
        else:

            prob_list = []
            for dclass in self.__document_classes:
                prob = self.probability(doc, dclass)
                prob_list.append([dclass, prob])
                prob_list.sort(key = lambda x: x[1], reverse=True)
            return prob_list

    def sum_words_in_class(self, dclass):
        """ Count of different words of a dclass """
        sum = 0
        for word in self._vocabulary.Words():
            waF = self.__document_classes[dclass].words_freq(word)
            sum += waF
        return sum
