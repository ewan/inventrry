from util import binary_counts
from util import otn

def imbalance(feature_values):
    '''
    	Return la différence entre le nombre de trait positif et le nombre de trait négatif
    	:param feature_values: Une Serie au format (1/-1)
    
    '''
    n_minus, n_plus = binary_counts(feature_values)
    if n_minus == 0 or n_plus == 0:
        return None
    else:
        return abs(n_minus - n_plus)

def nimbalance( values, spec ) :
	'''
		Calcule le nombre d'opposition total d'un inventaire aka le nombre de paires de phonèmes distincts d'un seul trait  
		
		:param values: l'inventaire au format (+/-) d'une langue  
		:param spec: une Serie de trait distinctif avec pour chacun un  boolean utilisé pour savoir si le trait est discriminant ou non.
		:return: le nombre d'opposition 
	'''
	trueSpec = []
	for i in spec.items() :
		if(i[1] == True):
			trueSpec.append(i[0])

	total = 0
	for i in trueSpec :
		total += imbalance(otn(values[i]))
	return total