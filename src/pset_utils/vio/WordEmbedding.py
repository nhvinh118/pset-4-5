# -*- coding: utf-8 -*-
import re
import os
from functools import reduce

from load_data import load_vectors, load_words, load_data

class WordEmbedding(object):
    def __init__(self, words, vecs):

        """ Initialize the class

        """
        self.words = words

        self.vecs = vecs

    def __call__(self, word):

        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray

        """

        # Append new line to word
        iword = word + '\n'
        try:
            vindex = self.words.index(iword)
            return self.vecs[vindex]
        except ValueError:
            return 0

    @classmethod
    def from_files(cls, word_file, vec_file):

        """Instanciate an embedding from files

        Example::
            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')
        :rtype: cls

        """
        
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        wfile = fileDir + '/data/' + word_file
        vfile = fileDir + '/data/' + vec_file

        return cls(load_words(wfile), load_vectors(vfile))

    def tokenize(self, text):
        # Get all "words", including contractions
        # eg tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
        
        return re.findall(r"\w[\w']+", text.lower())

    def embed_document(self, text):

        """Convert text to vector, by finding vectors for each word and combining (adding)

            Use tokenize(), and functools.reduce, itertools.aggregate...
            Assume any words not in the vocabulary are treated as 0's
            Return a zero vector even if no words in the document are part
            of the vocabulary

        :param str document: the document (one or more words) to get a vector
            representation for

        :return: vector representation of document
        :rtype: ndarray (1D)

        """
        # Tokenize the incomiung text
        intext = self.tokenize(text)
        # Use self.__call__(word) to vectorize the text then add them up
        textvector = reduce((lambda x=0, y=0: x if y is None else x + y), [self.__call__(word) for word in intext ])
        if textvector is None:
            textvector = 0
     
        return textvector
