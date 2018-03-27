from util import get_cols_except
from util import sebHash

from partition import to_row_partition

def mpairs2(inventory, spec, feature):
    '''
    	Calculate the number of phonem which are distinct only by the specified feature 
    	
    	:param inventory: A inventory of a langage
		:param spec: A string List representing discriminating features 
		:param feature: a specific feature which has to be tested
		:type inventory: pandas.DataFrame
		:type spec: List
		:type feature: String
    '''
    if inventory.shape[0] == 2 and len(spec) == 1:
        return 1
    partition = to_row_partition(get_cols_except(inventory, spec, feature))
    n_equivalence_classes = len(partition)
    return inventory.shape[0] - n_equivalence_classes

def mpairs(inventory, spec, feature):
    '''
    	Calculate the number of phonem which are distinct only by the specified feature 
    	
    	:param inventory: A inventory of a langage
		:param spec: A string List representing discriminating features 
		:param feature: a specific feature which has to be tested
		:type inventory: pandas.DataFrame
		:type spec: List
		:type feature: String
    '''
    if inventory.shape[0] == 2 and len(spec) == 1:
        return 1
    partition = get_cols_except(inventory, spec, feature).values.tolist()
    test = set()
    for i in partition : 
    	test.add(sebHash(i))
    return inventory.shape[0] - len(test)

def nmpairs(inventory, spec):
	'''
		Calculate the number of phonem which are distinct only by the specified feature 
    	
    	:param inventory: A inventory of a langage
		:param spec: A string List representing discriminating features 
		:type inventory: pandas.DataFrame
		:type spec: list
	'''
	return sum(mpairs(inventory, spec, feat) for feat in spec)
