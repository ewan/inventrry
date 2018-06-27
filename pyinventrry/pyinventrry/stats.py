__all__ = ['stat', 'econ', 'loc', 'glob']

from pyinventrry.score import ecovalue as _ev, mpairs as _mp, imbalance as _ib
import pyinventrry.util as _ut

def stat (inv, tspec, tab = None ) :
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
	if tab is not None :
		eco = econ(inv, tspec)
	loca = loc(inv, tspec, tab, normalize)
	globa = glob(inv, tspec, tab, normalize)
	if tab is not None :
		return (None, eco, loca, globa)
	return (inv.shape[0], len(tspec), loca, glob)

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

def loc (inv, tspec, tab = None) :  
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
	if tab is not None :
		return (_ut.norm_datas(nb_mpairs,tab, size, nfeat))
	return nb_mpairs
	
def glob (inv, tspec, tab = None) : 
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
	if tab is not None :
		return (_ut.norm_datas(nb_imbalance,tab, size, nfeat,nb_mpairs))
	return n_imbalance
