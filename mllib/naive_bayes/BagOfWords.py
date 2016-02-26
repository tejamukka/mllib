# !/usr/bin/env python

# BagoFWOrds store words with counts. It's an dictionary extension.

class BagOfWords(object):
    """ Bag of words represent dictionaries of words with respective count """
    def __init__(self):
        self._number_of_words = 0
        self._bag_of_words = {}

    def __add__(self, other):
        """ Overloading of the '+' operator to join two bag of words """
        erg = BagOfWords()
        sum = erg._bag_of_words
        for key in self._bag_of_words:
            sum[key] = self._bag_of_words[key]

            if key in other._bag_of_words:
                sum[key] += other._bag_of_words[key]

        for key in other._bag_of_words:
            if key not in sum:
                sum[key] = other._bag_of_words[key]
        return erg

    def __len__(self):
        """ Returning the number of different words in bag """
        return len(self._bag_of_words)

    def add_word(self, word):
        """ Adding word to bag """
        self._number_of_words += 1
        if word in self._bag_of_words:
            self._bag_of_words[word] += 1
        else:
            self._bag_of_words[word] = 1

    def word_freq(self, word):
        """ Return the frequency of word """
        if word in self._bag_of_words:
            return self._bag_of_words[word]
        else:
            return 0

    def Words(self):
        """ Returning a list of words contained in the object """
        return self._bag_of_words.keys()

    def BagOfWords(self):
        """ Returning the dictionary of words """
        return self._bag_of_words
