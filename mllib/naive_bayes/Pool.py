from mllib.naive_bayes.BagOfWords import BagOfWords
from mllib.naive_bayes.Category import Category
from mllib.naive_bayes.Document import Document

import os
import math
import re
from math import e

class Pool(object):
    def __init__(self):
        self.__document_classes = {}
        self._vocabulary = BagOfWords()
        self.__no_of_documents = 0
        self._stop_words = None
        self._weights = {}
        self.__document_classes_list = {}


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
            self.__document_classes_list.setdefault( dclass_name, [] ).append( d )

        self.__document_classes[dclass_name] = x
        self._vocabulary = self._vocabulary + x._vocabulary

        #print(self.__document_classes[dclass_name]._vocabulary.BagOfWords())
        x.SetNumberOfDocs(len(dir))

    def calculate(self, dclass, dclass_name):
        s = 0
        for keys in dclass._vocabulary.Words():
            s += self._weights[keys]

        r = (e**s)/(1+ e**s);
        return r

    def train(self, positive_class):
        iter = 3
        gamma = 0.08
        lamda = 0.5

        self._weights = self._vocabulary.BagOfWords()
        for keys in self._weights:
            self._weights[keys] = 0

        while(iter):
            r = 0
            for dclass, dlist in self.__document_classes_list.items():
                for document in dlist:

                    if dclass == positive_class:
                        document.setError(1 - self.calculate(document, dclass))
                    else:
                        document.setError(-self.calculate(document, dclass))
                    #print ("ERROR ", document.getError())

            for key in self._weights.keys():
                r = 0
                for dclass, dlist in self.__document_classes_list.items():
                    for document in dlist:
                    # find error
                        if key in document._vocabulary.BagOfWords():
                            r += document.getError()
                self._weights[key] += gamma*r - gamma*lamda*self._weights[key]

            iter -= 1
        #print(self._weights)

    def regression(self, doc,positive_class, negative_class):
        d = Document()
        d.read_document(doc, self._stop_words)

        r = 0
        for word in d._vocabulary.Words():
            if word in self._weights:
                r += self._weights[word]
        #print("value of r ", r)
        res = []
        if r > 0:
            res.append([positive_class, r],)
        else:
            res.append([negative_class, r],)

        return res

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
