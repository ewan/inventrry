import pandas as pd 
import mpairs as mp
import imbalance as ib
import util as ut

def stats (inv, tspec, tab) :
	'''

		Calculate the economic score, the local score and the global score

		:param inv: an inventory
		:param tspec: A string List representing discriminating features 
		:param tab: the normalization array
		:type inventory: pandas.DataFrame
		:type tspec: list
		:type tab: pandas.DataFrame
		:return: a tuple of score 
		:rtype: double tuple

	'''
	size = inv.shape[0]
	nfeat = len(tspec)
	nbMpairs = mp.nmpairs(inv, tspec)
	nbImbalance = ib.nimbalance(inv, tspec)
	econ = econValue(size, nfeat)
	loc = ut.normDatas(nbMpairs, tab, size, nfeat)
	glob = ut.normDatas(nbImbalance, tab, size, nfeat,nbMpairs)
	return (econ, loc, glob)

def econ(inv, tspec) : 
	'''
		Calcutate the economic score
		:param inv: an inventory
		:param tspec: A string List representing discriminating features 
		:type inventory: pandas.DataFrame
		:type tspec: list
		:return: the score
		:rtype: double

	'''
	size = inv.shape[0]
	nfeat = len(tspec)
	return econValue(size, nfeat)

def econValue(size, nfeat):
	"""
		Calculate the economic score from int values
		:param size: the size of an inventory
		:param nfeat: the number of discriminating features 
		:type size: int
		:type nfeat: int
		:return: the score
		:rtype: double
	"""
	return (size - (nfeat+1))/(2**nfeat - (nfeat+1))

def loc (inv, tspec, tab) :  
	'''
		Calcutate the local score
		:param inv: an inventory
		:param tspec: A string List representing discriminating features 
		:param tab: the normalization array
		:type inventory: pandas.DataFrame
		:type tspec: list
		:type tab: pandas.DataFrame
		:return: the score
		:rtype: double

	'''
	size = inv.shape[0]
	nfeat = len(tspec)
	nbMpairs = mp.nmpairs(inv, tspec)
	return (ut.normDatas(tab, size, nfeat))[nbMpairs]
	
def glob (inv, tspec, tab) : 
	'''
		Calcutate the global score
		:param inv: an inventory
		:param tspec: A string List representing discriminating features 
		:param tab: the normalization array
		:type inventory: pandas.DataFrame
		:type tspec: list
		:type tab: pandas.DataFrame
		:return: the score
		:rtype: double

	'''
	size = inv.shape[0]
	nfeat = len(tspec)
	nbMpairs = mp.nmpairs(inv, tspec)
	nbImbalance = ib.nimbalance(inv, tspec)
	return (ut.normDatas(tab, size, nfeat,nbMpairs))[nbImbalance]