import numpy as np
import sys
import argparse
import pandas as pd
import pyinventrry as pi
import pyinventrry.util as ut

def calculate_meta_keys(data_frame):
	'''
	Find all colummns name which start with an underscore
	:param data_frame: the DataFrame to analyse.
	:type data_frame: DataFrame
	:return: the list of all meta keys of the DataFrame
	:rtype: string array
	'''
	all = [ x for x in data_frame ]
	meta = []
	for k in all :
		if k=='' or k[0]=='_' :
			meta.append(k)
	return meta

def calculate_unique(data_frame, acc, meta):
	'''
	Calculate all unique meta_data tuples in a dataframe
	:param data_frame: The DataFrame to analyse
	:param acc: an accumulator with part of tuples already known
	:param meta: the list of yet unanalysed meta keys
	:type data_frame: DataFrame
	:type acc: A tuple array array
	:type meta: string array
	:return: the list of all unique meta_value in the DataFrame
	:rtype: tuple array array
	'''
	new_acc = []
	m_key = meta.pop()
	tmp = pd.DataFrame(data_frame)
	for k in acc :
		for tk in k :
			tmp = tmp.loc[tmp[tk[0]]==tk[1]]
		uni = tmp[m_key].unique()
		for n in uni :
			new_key = list(k)
			new_key.append((m_key,n))
			new_acc.append(new_key)
	if meta :
		return calculate_unique(data_frame, new_acc, meta)
	else :
		return new_acc

def extract_data_frame(data_frame, tuples):
	'''
	Extract the part of the DataFrame which matchs the meta_values given in argument
	:param data_frame: The DataFrame which is going to be parsed
	:param tuples: An array containing (k,v) tuples with k a columns name and v a value in this columns
	:type data_frame: DataFrame
	:type tuples: A tuple array
	:return: The part of  DataFrame corresponding to the tuples argument 
	:rtype: DataFrame
	'''
	ret = pd.DataFrame(data_frame)
	for t in tuples :
		ret = ret.loc[ret[t[0]]==t[1]]
		ret = ret.drop(t[0], axis=1)
	return ret

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
	meta_keys = calculate_meta_keys(inv_whole)
	if not meta_keys :
		print('There is an error in the inventory file as no meta information was detected.',file=sys.stderr)
		return 
	meta_keys_spec = calculate_meta_keys(spec_whole)
	if not meta_keys_spec :
		print('There is an error in the specification file as no meta information was detected',file=sys.stderr)
		return
	delta_keys = list(set(meta_keys_spec) - set(meta_keys))
	unique = calculate_unique(inv_whole,[[]], list(meta_keys))
	result_global = pd.DataFrame(columns=meta_keys + delta_keys + ['econ','loc','glob'])
	result_global.to_csv(write_file,index=False)
	for t in unique:
		inv = extract_data_frame(inv_whole, t)
		spe = extract_data_frame(spec_whole, t)
		spec_keys = calculate_unique(spe, [[]], list(delta_keys))
		for s_key in spec_keys :
			 
			result = pd.DataFrame(columns=meta_keys + delta_keys +['econ','loc','glob'])
			x = (extract_data_frame(spe,s_key))
			e, l, g = pi.stats.stat(inv, (ut.get_true_specs(x.iloc[0].to_dict())),norm_tab)
			d = dict(t+s_key)
			d['econ'] = e
			d['loc'] = l
			d['glob'] = g
			result = result.append(d, ignore_index=True)
			result.to_csv(write_file, mode = 'a', header=False, index=False)

def open_file(argument):
	'''
	Check file type and open it correctly
	:param argument: The path to the file
	:type argument: string
	:return: the corresponding DataFrame
	:rtype: DataFrame
	'''
	if (argument[-3:]=='csv'):
		return pd.read_csv(argument)
	else :
		return pd.read_feather(argument)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A file with the correct format for the inventory')
	parser.add_argument("specs", help = 'A file with the correct format for the specs')
	parser.add_argument("norm_tab", help = 'A file used for normalize data')
	parser.add_argument("-w", "--write", default=sys.stdout,)
	args = parser.parse_args(sys.argv[1:])
	calculate_score(	open_file(args.inventory),
			open_file(args.specs), 
			open_file(args.norm_tab),
			args.write)

if __name__ == "__main__":
	main()
