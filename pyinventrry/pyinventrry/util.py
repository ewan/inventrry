'''
Created on 2015-05-18

@author: emd
'''

import numpy as _np

def seb_hash( tab ) : 
	'''
	Calculate the hash of a (+/-) array
	:param tab: the array to hash
	:type tab: String array
	:return: the hash value
	:rtype: int
	'''
	l = len(tab)
	r = 1
	for i in range(l) :
		r = r*10
		if tab[i] == '-':
			r+=1
	return r

def norm_datas(value, normTab, size, nfeat, nmpairs = None):
	'''
		Normalize a array of values into its [0-1] equivalent. If nmpairs has only one possibility and nimbalance is asked, return None 
		:param value: the value to normalize 
		:param normTab: the normalization array
		:param size: index
		:param nfeat: index
		:param nmpairs: optional index
		:type value: int
		:type normTab: pandas.DataFrame
		:type size: int
		:type nfeat: int
		:type nmpairs: int
		:return: the dictionnary which associtate each number with a 0-1 double 
		:rtype: dictionarry

	'''
	if nmpairs is None :
		dictValues = normTab.loc[
			(normTab["size"] == size) 
			& (normTab["nfeat"] == nfeat), "nmpairs"].tolist()
	else : 
		dictValues = normTab.loc[
			(normTab["size"] == size) 
			& (normTab["nfeat"] == nfeat) 
			& (normTab["nmpairs"] == nmpairs), "nimbalance"].tolist()
	normList = sorted(set(dictValues))
	length = len(normList)
	if length == 1 :
		return _np.nan
	return normList.index(value)/(length-1)

def get_true_specs(dictio):
	'''
		Wipe out all entries of a dictionnay which are not exactly True 
		:param dictio: the dictionnary to clean
	'''
	tmp = []
	for f in dictio :
		if ((type(dictio[f]) == _np.bool_) or (type(dictio[f]) == bool)):
			if(dictio[f]):
				tmp.append(f)
	return tmp

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
		:param matrix: A language inventory
		:param cols: the cols to get.
		:param no_go_col: the string to remove of the cols.
		:type matrix: pandas.DataFrame
		:type cols: List
		:type no_go_col: string
	'''
	cols_to_get = tuple([c for c in cols if c != no_go_col])
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
	values = _np.unique(vec)
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

