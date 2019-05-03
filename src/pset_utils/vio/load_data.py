# -*- coding: utf-8 -*-
import os
from io import IOBase

import numpy as np
import pandas as pd


def load_words(filename):

    """Load a file containing a list of words as a python list
    :param str filename: path/name to file to load, file should have one line per word
	:rtype: list
    :raises: FileNotFoundError if filename does not exist

    """

    ilines = ""
    try:
        with open(filename,'r') as f:
            ilines = f.readlines()
        return ilines
    except FileNotFoundError as ferror:
        print (ferror)


def load_vectors(filename):

    """Loads a file containing word vectors to a python numpy array
    :param filename: path/name to .npy file
    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding
    :rtype: ndarray
    :raises: FileNotFoundError if filename does not exist

    """
    
    m = n = 0
    loaded_matrix = np.empty((m,n))
    try:
        loaded_matrix = np.load(filename, mmap_mode ='r')
        return loaded_matrix
    except FileNotFoundError as ferror:
        print (ferror)
		
def load_data(in_file):

    """Load student response data in parquet format
    :param str filename: path/name to .parquet file
    :returns: dataframe indexed on a hashed github id, empty cells with be filled with NaN
    :rtype: DataFrame
    :raises: FileNotFoundError if filename does not exist

    """
    
    base_infile = ext_infile = ''
    if isinstance(in_file, IOBase):
        base_infile, ext_infile = os.path.splitext(in_file.name)
    else:
        base_infile, ext_infile = os.path.splitext(in_file)

    assert base_infile !='', "Invalid file name"
    try:
        if ext_infile == '.parquet':
            df = pd.read_parquet(in_file, engine='pyarrow')
        elif ext_infile == '.xlsx':    
            df = pd.read_excel(in_file)
        else:
            print("Unsupported file type")
            return None
        # Fill NaN with 0
        odf = df.fillna(0)
        return odf
    except FileNotFoundError as ferror:
        print (ferror)	
