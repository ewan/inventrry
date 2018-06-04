import spec as _sp
import data_manager as _dm
import numpy as _np
import timeit as _ti
import sys as  _sys
import argparse
import pandas as _pd

def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped

def calculate_one (feat_set, phones, feat_dict, df_phones):
	int_specs = _sp.tree_theory(feat_set, [phones])
		
	specs = []
	for int_spec in int_specs :
		spec = set()
		for i in int_spec:
			spec.add(feat_dict[i])
		if _sp.check_spec(spec, df_phones):
			specs.append(spec)
	return specs


def time_specs(file_name) :	
	inventories, meta_keys, unique_list, feat_list = _sp.extract_from_file(file_name)
	feat_dict = _sp.calculate_feat_dict(feat_list)
	feat_set = set(feat_dict)
	time_dict = {}
	for unique in unique_list :
		df_phones = _dm.extract_data_frame(inventories, unique)
		phones = _sp.extract_phones(df_phones, feat_dict )
		
		wrapped = wrapper(calculate_one,feat_set,phones,feat_dict,df_phones)
		size = len(phones)
		time = _ti.timeit(wrapped,setup ="gc.enable"  ,number =1)
		if size in time_dict :
			time_dict[size].append(time)
		else :
			time_dict[size] = [time]
	df = _pd.DataFrame(columns=['Size','Median','Variance'])
	
	for s in time_dict:
		print(s)
		d = {'Size' : s,'Median' :_np.median(time_dict[s]),'Variance' : _np.var(time_dict[s])}
		print(d)
		df = df.append(d, ignore_index=True)

	return df.sort_values('Size')



def main() :
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A file with the correct format for the inventory')
	parser.add_argument("-w", "--write", default=_sys.stdout)
	args = parser.parse_args(_sys.argv[1:])
	file_name = args.inventory
	write_file = args.write
	df = time_specs(file_name)
	df.to_csv(write_file, mode = 'w', header=True, index=False)
	print(df)
		
if __name__ == "__main__":
	main()