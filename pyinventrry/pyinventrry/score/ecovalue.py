def econ_value(size, nfeat):
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
