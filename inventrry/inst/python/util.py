'''
Created on 2015-05-18

@author: emd
'''

import numpy as np

def clean(dictio):
    '''
        Wipe out all entries of a dictionnay which are not exactly True or False 
        :param dictio: the dictionnary to clean
    '''
    tmp = []
    for f in dictio :
        if ((str(dictio[f]) != "True") and (str(dictio[f]) != "False") ):
            tmp.append(f)
    for k in tmp:
        dictio.pop(k,None)

def otn(operators):
    '''
        Trasforme une Serie au format (+/-) en une Serie au format(1/-1)

        :param operators: Une Serie au format (+/-)
        :return: Une Serie au format (1/-1)

    '''
    k = operators
    k = k.replace(to_replace = '+', value=1)
    k = k.replace(to_replace = '-', value=-1)
    return k

def get_cols_except(matrix, cols, no_go_col):
    '''
        :param matrix:
        :param cols:
        :param no_go_col:
    '''
    cols_to_get = tuple([c for c in cols.keys() if c != no_go_col])
    return matrix.loc[:,cols_to_get]

def binary_counts(vec):
    '''
    vec is assumed to be binary and contain either -1/1,
    0/1, or 0/-1. If the values are -1/1, the first returned element
    is the number of -1's, and the second element is the number of 1's.
    If there is a 0, the first returned element is always the number
    of 0's. (This is true even if the other value is -1, in which
    case, downstream, BalanceIterator will put the number of 0's as
    the "minus count" and the number of -1's as the "plus count",
    which is why the variables in this function have the names
    that they do.)
    '''
    values = np.unique(vec)
    if len(values) > 2:
        raise ValueError()
    if len(values) == 2 and values[0] == 0:
        minus_val = 0
    else:
        minus_val = -1
    is_minus = vec == minus_val
    return sum(is_minus), sum(~is_minus)
        
def spec_id(feature_set, feature_names):
    feat_name_strings = [feature_names[c] for c in feature_set]
    return "'" + ":".join(feat_name_strings) + "'"

