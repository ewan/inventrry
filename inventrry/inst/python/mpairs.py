from util import get_cols_except
from partition import to_row_partition

def mpairs(inventory, spec, feature):
    '''
    
    '''
    if inventory.shape[0] == 2 and len(spec) == 1:
        return 1
    partition = to_row_partition(get_cols_except(inventory, spec, feature))
    n_equivalence_classes = len(partition)
    return inventory.shape[0] - n_equivalence_classes

def nmpairs(inventory, spec):
	trueSpec = [f for f in spec.iloc[:][4:27].keys() if spec.iloc[:][f]]
	
	return sum(mpairs(inventory, spec[4:27], feat) for feat in trueSpec)
