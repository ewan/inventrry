import sys
import argparse
import numpy as np
from partition import PartitionCached

def collapse(s):
    """
    Args:
        s (list): A list of collections
    Returns:
        A list containing all the unique elements of any collection in `s`
    """
    result = []
    for x in s:
        result += [e for e in x if e not in result]
    return result

def contained_one(s, sets):
    for e in sets:
        if s.issubset(e):
            return True
    return False
 
def contains_one(s, sets):
    for e in sets:
        if s.issuperset(e):
            return True
    return False
    
def is_full_rank(s, partitions):
    return len(partitions.get(s)) == partitions.table.shape[0]

def is_rank_more_than_one(s, partitions):
    partition = partitions.get(s)
    rank = len(partition)
    return rank > 1

def is_rank_increase(s, f, partitions):
    partition_1 = partitions.get(s)
    partition_2 = partitions.split(s, f)
    rank1 = len(partition_1)
    rank2 = len(partition_2)
    if rank2 > rank1:
        return True
    return False

def is_not_rank_decrease(s, f, partitions):
    partition_1 = partitions.get(s)
    partition_2 = partitions.collapse(s, f)
    rank1 = len(partition_1)
    rank2 = len(partition_2)
    if rank2 == rank1:
        return True
    return False

# Subsampled expansion

def filter_subsample(sets, n, unexplored, explored, seed):
    """
    Args:
        sets (list): Sets of features
        n (int): Size of the subsample of `sets` to take
        unexplored (list): Known unexplored sets
        explored (list): Known explored (minimal) sets
        seed (int or None): Optional random seed
    Returns:
        A tuple `subset, new_unexplored`:
            subset (list): A random subset of `sets` of size no more than
                `min(n, len(sets))` which contains only sets that are not in
                `explored`
            new_unexplored (list): A list of elements of `sets` that are not
                supersets of any set in `unexplored`, but for which
                we cannot guarantee that they are either
                    * in `subset`, or
                    * in `explored`
    """
    np.random.seed(seed)
    np.random.shuffle(sets)
    subset_indices = []
    window_start = 0
    n_remaining = n
    window_end = n
    while len(subset_indices) < n and window_start < len(sets):
        window = range(window_start, window_end)
        included = [i for i in window if sets[i] not in explored]
        subset_indices += included
        n_remaining = n - len(subset_indices)
        window_start = window_end
        window_end = min(window_start + n_remaining, len(sets))
    subset = [sets[i] for i in subset_indices]
    if window_end < len(sets):
        remaining = sets[window_end:]
        new_unexplored = [s for s in remaining if contains_one(s, unexplored)]
    else:
        new_unexplored = []
    return subset, new_unexplored

def add_all(s, features, explored, partitions):
    """
    Args:
        s (set): A set of features
        features (list): All features that can be added to expand a set
        explored (list): Known explored (minimal) sets
        partitions (PartitionCached): Cached partitions of the inventory
    Returns:
        List of all supersets of `s` which can be reached by adding just
        one feature, provided they
            * are not supersets of `explored`
            * add some segments beyond those already picked out by `s`
            * can specify the inventory
    """
    result = [s | set([f]) for f in features if
              not f in s and
              not contains_one(s | set([f]), explored) and
              is_rank_increase(s, f, partitions) and
              is_rank_more_than_one(s | set([f]), partitions)]
    return result

def add_all_collapse(sets, features, explored, partitions):
    """
    Args:
        sets (list): Sets of features
        features (list): All features that can be added to expand a set
        explored (list): Known explored (minimal) sets
        partitions (PartitionCached): Cached partitions of the inventory
    Returns:
        sets: A list of sets that can specify the inventory, each one an
                expansion by one feature of one of the sets in `s` that
                adds at least one segment to the extension; guaranteed
                never to be a superset of one of the sets listed in `explored`
    """
    applied = [add_all(x, features, explored, partitions) for x in sets]
    return collapse(applied)

def filter_add_all_collapse(sets, features, explored, partitions):
    """
    Like `add_all_collapse` but pre-filters `sets` to check that none is a
    in `explored`.
    """
    applied = [add_all(x, features, explored, partitions) for x in sets if
                    x not in explored]
    return collapse(applied)
        
def subsampled_expand(sets, max_num_sets, unexplored, explored, features,
                        partitions, seed):
    """
    Args:
        sets (list): Sets of features
        max_num_sets (int): Maximum number of sets from `sets` to expand
        unexplored (list): Known unexplored sets
        explored (list): Known explored (minimal) sets
        features (list): All features that can be added to expand a set
        partitions (PartitionCached): Cached partitions of the inventory
        seed (int or None): Optional seed for subsampling
    Returns:
        A tuple `sets, unexplored`
            sets: A list of sets that can specify the inventory, each one an
                    expansion by one feature of one of the sets in `sets` that
                    adds at least one segment to the extension;
                    guaranteed never to be a superset
                    of one of the sets listed in `explored`; guaranteed to be
                    exhaustive only if `max_num_sets == inf`
            unexplored: An updated list of sets known to be unexplored (the
                    ones left out by subsampling to comply with `max_num_sets`
                    which are not themselves supersets of previously unexplored
                    sets)
    """
    if len(sets) <= max_num_sets:
        sets_ = filter_add_all_collapse(sets, features, explored, partitions)
        unexplored_ = unexplored
    else:
        sets_subsample, newly_unexplored = filter_subsample(
                                                sets,
                                                max_num_sets,
                                                unexplored,
                                                explored,
                                                seed)
        sets_ = add_all_collapse(sets_subsample, features, explored, partitions)
        unexplored_ = unexplored + newly_unexplored
    return (sets_, unexplored_)
    
# Minimal specification search

def is_feasible_unexplored(s, unexplored, explored, infeasible, partitions):
    return contains_one(t, unexplored) and \
           is_rank_more_than_one(t, partitions) and \
           not contains_one(t, explored) and \
           not contained_one(t, infeasible) and \
           is_not_rank_decrease(s, f, partitions)

def can_contract(s, unexplored, explored, infeasible, partitions):
    has_feasible = False
    infeasible_ = []
    for f in s:
        t =  s - set(f)
        if is_feasible_unexplored(t, unexplored, explored, infeasible,
                partitions):
            has_feasible = True
            break
        else:
            infeasible_.append(t)
    return has_feasible, infeasible_

def contract(s, unexplored, explored, infeasible, partitions):
    feasible = []
    infeasible_ = []
    for f in s:
        t =  s - set(f)
        if is_feasible_unexplored(t, unexplored, explored, infeasible,
                partitions):
            feasible.append(t)
        else:
            infeasible_.append(t)
    return feasible, infeasible_
   
def contract_all_collapse(sets, unexplored, explored, infeasible, partitions):
    contractions = []
    infeasible_ = []
    for s in sets:
        feasible, new_infeasible = contract(s, unexplored, explored, infeasible,
                                        partitions)
        contractions.append(feasible)
        infeasible_ += new_infeasible
    return collapse(contractions), infeasible_
    

def top_down_search(sets, unexplored, explored, infeasible, partitions):
    """
    Args:
        sets (list): Sets of features
        unexplored (list): Known unexplored sets
        explored (list): Known explored (minimal) sets
        infeasible (list): Known explored (minimal) sets
        partitions (PartitionCached): Cached partitions of the inventory
    Returns:
        A tuple `(minimal, infeasible_)`:
            minimal (list): Newly discovered minimal sets
            infeasible_ (list): Updated list of non-specifications
    """
    minimal = []
    unknown = []
    new_infeasible = []
    for s in sets:
        has_feasible, infeasible_subsets = can_contract(
                                                s,
                                                unexplored,
                                                explored,
                                                infeasible,
                                                partitions)
        new_infeasible += infeasible_subsets
        if not has_feasible:
            minimal.append(s)
        else:
            unknown.append(s)
    while unknown:
        for s in unknown:
            has_feasible, infeasible_subsets = can_contract(
                                                    s,
                                                    unexplored,
                                                    explored,
                                                    infeasible,
                                                    partitions)
            new_infeasible += infeasible_subsets
            if not has_feasible:
                minimal.append(s)
            unknown, infeasible_subsets = contract_all_collapse(
                                                    unknown,
                                                    unexplored,
                                                    explored,
                                                    infeasible,
                                                    partitions)
            new_infeasible += infeasible_subsets
    return minimal, infeasible + new_infeasible

def minimal_set_exploration(sets, unexplored, explored, infeasible, partitions):
    """
    Args:
        sets (list): Sets of features
        unexplored (list): Known unexplored sets
        explored (list): Known explored (minimal) sets
        infeasible (list): Known non-specifications
        partitions (PartitionCached): Cached partitions of the inventory
    Returns:
        A tuple `(minimal, explored_, infeasible_)`:
            minimal (list): Newly discovered minimal sets
            explored_ (list): `explored` + `minimal`
            infeasible_ (list): Updated list of non-specifications
    """
    candidates = [s for s in sets if is_full_rank(s, partitions)]
    if unexplored:
        unknown = []
        minimal_ = []
        for s in candidates:
            if contains_one(s, unexplored):
                unknown.append(s)
            else:
                minimal_.append(s)
        if unknown:
            new_minimal, new_infeasible = top_down_search(unknown,
                                              explored,
                                              infeasible,
                                              partitions)
            minimal_ += new_minimal
            infeasible_ = infeasible + new_infeasible
    else:
        minimal_ = candidates
        infeasible_ = infeasible
    return minimal_, explored + minimal_, infeasible_
 
class MinimalSetIterator(object):
    """
    Iterator over minimal sets of features for an inventory.
    Performs approximate bottom-up search. If `max_cost` is less
    than `inf`, the results may not be exhaustive.
    
    ```
    Sets := [{}]
    Minimal := []
    Unexplored := []
    Maximum Number of Sets to Expand :=
        Maximum Cost / Number of rows in Inventory
    iterate:
        if Minimal is empty:
            Sets, Unexplored := Subsampled Expansion of Sets (see above)
            while Subsets is not empty:
                Minimal, Explored := Minimal Set Exploration (see above)
                if Minimal is not empty:
                    BREAK
                else:
                    Sets, Unexplored := Subsampled Expansion of Sets
            if Minimal is empty:
                STOP
        YIELD an element of Minimal
    ```
    
    Args:
        inventory (numpy.array): A table with rows corresponding to sounds
            and columns corresponding to features.
        max_cost (float): See above
        seed (int or None): Optional seed for subsampling Sets
            (see above)
    """
    
    def __init__(self, inventory, max_cost, seed):
        self.sets = [set()]
        self.minimal = []
        self.unexplored = []
        self.explored = []
        self.infeasible = []
        self.features = range(inventory.shape[1])
        if max_cost < inventory.shape[0]:
            raise ValueError()
        self.max_num_sets_to_expand = max_cost / inventory.shape[0]
        self.partitions = PartitionCached(inventory)
        self.seed = seed
    
    def __iter__(self):
      return self
    
    def __next__(self):
        """
        Return the next minimal set of features. Stop if no more can
        be found.
        
        Returns:
            set: Column indices for `inventory` that correspond
                to a minimal set of features
        """
        if not self.minimal:
            self.sets, self.unexplored = subsampled_expand(
                                            self.sets,
                                            self.max_num_sets_to_expand,
                                            self.unexplored,
                                            self.explored,
                                            self.features,
                                            self.partitions,
                                            self.seed)
            while self.sets:
                self.minimal, self.explored, self.infeasible = \
                    minimal_set_exploration(self.sets,
                                            self.unexplored,
                                            self.explored,
                                            self.infeasible,
                                            self.partitions)
                if self.minimal:
                    break
                else:
                    self.sets, self.unexplored = subsampled_expand(
                                                    self.sets,
                                                    self.max_num_sets_to_expand,
                                                    self.unexplored,
                                                    self.explored,
                                                    self.features,
                                                    self.partitions,
                                                    self.seed)
            if not self.minimal:
                raise StopIteration()
        return self.minimal.pop()

def specs(inventory, max_cost, seed):
    if max_cost < float("inf"):
        max_cost = int(max_cost)
    if seed is not None:
        seed = int(seed)
    ms_iterator = MinimalSetIterator(inventory, max_cost, seed)
    indices = range(inventory.shape[1])
    result = []
    for ms in ms_iterator:
        result.append(list(ms))
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-cost', type=float,
                        default=float("inf"))
    parser.add_argument('--seed', type=int, default=None)
    parser.add_argument('inventory_fn',
                        help='csv containing features for a single inventory,'
                        ' with header, coded numerically')
    args = parser.parse_args(sys.argv[1:])
    inventory = np.genfromtxt(args.inventory_fn, delimiter=',', names=True)
    nfeat = len(inventory.dtype)
    feature_names = inventory.dtype.names
    inventory.dtype = None
    nsegs = len(inventory)//nfeat
    inventory.shape = (nsegs,23)
    specs_ = specs(inventory, args.max_cost, args.seed)
    row = ""
    prefix = ""
    for fname in feature_names:
        row += prefix + fname
        prefix = ","
    for s in specs_:
        row = ""
        prefix = ""
        for i in range(len(feature_names)):
            if i in s:
                row += prefix + "T"
            else:
                row += prefix + "F"
            prefix = ","
