import numpy as np
import sys
import argparse
import pandas as pd
import pyinventrry as pi
import pyinventrry.util as ut
import pyinventrry.data_manager as dm

def calculate_score( inv_whole, spec_whole, norm_tab, write_file ) : 
	'''
	Calculate and print economic, local and global scores.
	:param inv_whole:
	:param spec_whole:
	:param norm_tab:
	:param write_file:
	:type inv_whole:
	:type spec_whole:
	:type norm_tab:
	:type write_file:
	'''
	meta_keys = dm.calculate_meta_keys(inv_whole)
	if not meta_keys :
		print('There is an error in the inventory file as no meta information was detected.',file=sys.stderr)
		return 
	meta_keys_spec = dm.calculate_meta_keys(spec_whole)
	if not meta_keys_spec :
		print('There is an error in the specification file as no meta information was detected',file=sys.stderr)
		return
	delta_keys = list(set(meta_keys_spec) - set(meta_keys))
	unique = dm.calculate_unique(inv_whole,[[]], list(meta_keys))
	result_global = pd.DataFrame(columns=meta_keys + delta_keys + ['econ','loc','glob'])
	result_global.to_csv(write_file,index=False)
	for t in unique:
		inv = dm.extract_data_frame(inv_whole, t)
		spe = dm.extract_data_frame(spec_whole, t)
		spec_keys = dm.calculate_unique(spe, [[]], list(delta_keys))
		for s_key in spec_keys :
			result = pd.DataFrame(columns=meta_keys + delta_keys +['econ','loc','glob'])
			x = (dm.extract_data_frame(spe,s_key))

			e, l, g = pi.stats.stat(inv, (ut.get_true_specs(x.iloc[0].to_dict())),norm_tab)
			d = dict(t+s_key)
			d['econ'] = e
			d['loc'] = l
			d['glob'] = g
			result = result.append(d, ignore_index=True)
			result.to_csv(write_file, mode = 'a', header=False, index=False)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A file with the correct format for the inventory')
	parser.add_argument("specs", help = 'A file with the correct format for the specs')
	parser.add_argument("norm_tab", help = 'A file used for normalize data')
	parser.add_argument("-w", "--write", default=sys.stdout,)
	args = parser.parse_args(sys.argv[1:])
	calculate_score(	dm.open_file(args.inventory),
			dm.open_file(args.specs), 
			dm.open_file(args.norm_tab),
			args.write)

if __name__ == "__main__":
	main()
