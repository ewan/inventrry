__all__ = ['stat', 'econ', 'loc', 'glob']

from pyinventrry.score import ecovalue as _ev, mpairs as _mp, imbalance as _ib
import pyinventrry.util as _ut

def stat (inv, tspec, tab) :
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
	eco = econ(inv, tspec)
	loca = loc(inv, tspec, tab)
	globa = glob(inv, tspec, tab)
	return (eco, loca, globa)

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
	return _ev.econ_value(size, nfeat)

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
	nb_mpairs = _mp.n_mpairs(inv, tspec)
	return (_ut.norm_datas(nb_mpairs,tab, size, nfeat))
	
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
	nb_mpairs = _mp.n_mpairs(inv, tspec)
	if _ut.norm_datas(nb_mpairs,tab, size, nfeat) is None :
		return None
	nb_imbalance = _ib.n_imbalance(inv, tspec)
	return (_ut.norm_datas(nb_imbalance,tab, size, nfeat,nb_mpairs))
