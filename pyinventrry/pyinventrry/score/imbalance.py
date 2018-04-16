from pyinventrry.util import binary_counts as _bc, otn as _otn

def imbalance(feature_values):
    '''
    	Return the difference between the number of plus and minus in a Serie
    	:param feature_values: Une Serie au format (1/-1)
    
    '''
    n_minus, n_plus = _bc(feature_values)
    if n_minus == 0 or n_plus == 0:
        return None
    else:
        return abs(n_minus - n_plus)

def nimbalance( values, spec ) :
	'''
		
		:param values: l'inventaire au format (+/-) d'une langue  
		:param spec: A string List representing discriminating features 
		:return: le nombre d'opposition 
	'''
	total = 0
	for i in spec :
		total += imbalance(_otn(values[i]))
	return total
