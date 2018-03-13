from util import get_cols_except
from partition import to_row_partition

def mpairs(inventory, spec, feature):
    '''
    	:param inventory:
		:param spec:
		:param feature:
		:type inventory: pandas.DataFrame
		:type spec: Dictionary
		:type feature: String
    '''
    if inventory.shape[0] == 2 and len(spec) == 1:
        return 1
    tmp = get_cols_except(inventory, spec, feature)
    #print(tmp)
    partition = to_row_partition(get_cols_except(inventory, spec, feature))
    n_equivalence_classes = len(partition)
    return inventory.shape[0] - n_equivalence_classes

def nmpairs(inventory, spec):
	'''
		:param inventory:
		:param spec:
		:type inventory: pandas.DataFrame
		:type spec: Dictionary
	'''
	trueSpec = [f for f in spec.keys() if spec[f]]
	return sum(mpairs(inventory, spec, feat) for feat in trueSpec)
