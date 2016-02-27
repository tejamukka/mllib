
from mllib.naive_bayes.BagOfWords import BagOfWords
import re

class Document(object):
    """ Represents a single document provided for training as well as for testing """

    def __init__(self):
        self._name = ""
        self._vocabulary = BagOfWords()
        self._error = 0

    def read_document(self, filename, stopwords=None):
        """ A document is read. It is assumed and parsed to find suitable words and
            used in bag of words """
        try:
            text = open(filename,"r", encoding='utf-8').read()
        except UnicodeDecodeError:
            text = open(filename,"r", encoding='latin-1').read()
        text = text.lower()

        words = re.split("(?:(?:[^a-zA-Z]+')|(?:'[^a-zA-Z]+))|(?:[^a-zA-Z']+)",text)[:-1]

        # only for regression
        words.append("BIASPUNEET")
        for word in words:
            if stopwords and word in stopwords:
                continue
            self._vocabulary.add_word(word)

    def __add__(self, other):
        """ Overloading the '+' operator. Adding two documents consists in adding the BagOfWords of the documents """
        res = Document(Document._vocabulary)
        res.vocabulary = self._vocabulary + other._vocabulary
        return res

    def vocabulary_length(self):
        """ Returning the length of vacabulary """
        return len(self._vocabulary)

    def words_freq(self, word):
        """ Returning the number of times word appeared in the document """
        return self._vocabulary.word_freq(word)

    def BagOfWords(self):
        """ Returning bag of words for a document """
        return self._vocabulary.BagOfWords()

    def Words(self):
        """ Returning the words of the document object """
        d = self._vocabulary.BagOfWords()
        return d.keys()

    def setError(self, error):
        self._error = error

    def getError(self):
        return self._error
