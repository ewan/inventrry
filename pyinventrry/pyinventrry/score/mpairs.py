from pyinventrry.util import sebHash as _sh, get_cols_except as _gce

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
    partition = _gce(inventory, spec, feature).values.tolist()
    test = set()
    for i in partition : 
    	test.add(_sh(i))
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
