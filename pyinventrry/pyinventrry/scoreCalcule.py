import sys
import argparse
import pandas as _pd
import pyinventrry as _pi
import pyinventrry.util as _ut
import pyinventrry.data_manager as _dm

def calculate_score( inv_whole, spec_whole, norm_tab, write_file ) : 
	'''
	Calculate and print economic, local and global scores of multiple inventories.
	:param inv_whole: The DataFrame regrouping all inventories.
	:param spec_whole: The DataFrame regrouping all specifications for these inventories.
	:param norm_tab: The normalization tab.
	:param write_file: the destination for writting results
	:type inv_whole: DataFrame
	:type spec_whole: DataFrame
	:type norm_tab: DataFrame
	:type write_file: str
	'''
	meta_keys = _dm.calculate_keys(inv_whole)
	
	meta_keys_spec = _dm.calculate_keys(spec_whole)
	
	delta_keys = list(set(meta_keys_spec) - set(meta_keys))
	unique = _dm.calculate_unique(inv_whole,[[]], list(meta_keys))
	result_global = _pd.DataFrame(columns=meta_keys + delta_keys + ['econ','loc','glob'])
	result_global.to_csv(write_file,index=False)
	
	for t in unique:
		inv = _dm.extract_data_frame(inv_whole, t)
		spe = _dm.extract_data_frame(spec_whole, t)
		spec_keys = _dm.calculate_unique(spe, [[]], list(delta_keys))
		for s_key in spec_keys :
			result = _pd.DataFrame(columns=meta_keys + delta_keys +['econ','loc','glob'])
			x = (_dm.extract_data_frame(spe,s_key))
			d = dict(t+s_key)
			s, e_f, l, g = _pi.stats.stat(inv, (_ut.get_true_specs(x.iloc[0].to_dict())),norm_tab)
			if norm_tab is None :
				d['size'] = e_f
				d['nfeat'] = s
				d['nmpairs'] = l
				d['nimbalance'] = g
			else :
				d['econ'] = e_f
				d['loc'] = l
				d['glob'] = g
			result = result.append(d, ignore_index=True)
			result.to_csv(write_file, mode = 'a', header=False, index=False)

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument("inventory",
		help = 'A file with the correct format for the inventory')
	parser.add_argument("specs",
		help = 'A file with the correct format for the specs')
	parser.add_argument(" -n", "--norm_tab", default = None
		help = 'A file used for normalize data')
	parser.add_argument("-w", "--write", default=sys.stdout,
		help = 'The path to the file where results will be written. ')

	args = parser.parse_args(sys.argv[1:])
	
	calculate_score(	_dm.open_file(args.inventory),
			_dm.open_file(args.specs), 
			_dm.open_file(args.norm_tab),
			args.write)

if __name__ == "__main__":
	main()
