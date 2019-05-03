import numpy as np

def cosine_similarity (a, b):

    """ Computes cosine similarity for two vector inputs. 
        cosine(X, Y) = <X, Y> / (||X||*||Y||)
        :param vector a, b: vectors to calculate cosine for
        :returns: cosine of a, b

    """
    if a is None:
        a = 0
    if b is None:
        b = 0

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    adotb  = np.dot(a,b)

    return adotb / (norm_a * norm_b)

def cos_distance (a,b):
    return 1 - cosine_similarity (a,b)
