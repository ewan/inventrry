from util import binary_counts
from util import otn

def imbalance(feature_values):
    '''
    
    '''
    n_minus, n_plus = binary_counts(feature_values)
    if n_minus == 0 or n_plus == 0:
        return None
    else:
        return abs(n_minus - n_plus)

def nimbalance( values, specs ) :
	trueSpec = []

	total = 0
	for i in trueSpec :
		total+= binary_counts(otn(values[i]))
	return total
	    
