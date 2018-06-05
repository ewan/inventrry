import spec as _sp
import data_manager as _dm
import numpy as _np
import timeit as _ti
import sys as  _sys
import argparse
import pandas as _pd

_ti.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

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

def time_specs(file_name, write_time, write_specs) :	
	inventories, meta_keys, unique_list, feat_list = _sp.extract_from_file(file_name)
	feat_dict = _sp.calculate_feat_dict(feat_list)
	feat_set = set(feat_dict)
	time_dict = {}
	df = _pd.DataFrame(columns=meta_keys + ['_spec_nb'] + feat_list)
	df.to_csv(write_specs, mode = 'w', header=True, index=False)
	
	for unique in unique_list :
		df_phones = _dm.extract_data_frame(inventories, unique)
		phones = _sp.extract_phones(df_phones, feat_dict )
		
		wrapped = wrapper(calculate_one,feat_set,phones,feat_dict,df_phones)
		size = len(phones)
		
		time, specs = _ti.timeit(wrapped,setup ="gc.enable"  ,number =1)
		
		if size in time_dict :
			time_dict[size].append(time)
		else :
			time_dict[size] = [time]

		i = 1
		for spec in specs :
			d = dict(unique)
			d['_spec_nb'] = 'Spec'+str(i)
			i+=1
			for feat in feat_list:
				d[feat] = False
			for t in spec:
				d[t] = True
			df = df.append(d, ignore_index=True)
		df.iloc[df.shape[0]-len(specs):df.shape[0]].to_csv(write_specs, mode = 'a', header=False, index=False)


	time_frame = _pd.DataFrame(columns=['Size','Median','Variance'])
	
	for s in time_dict:
		d = {'Size' : s,'Median' :_np.median(time_dict[s]),'Variance' : _np.var(time_dict[s])}
		time_frame = time_frame.append(d, ignore_index=True)

	return time_frame.sort_values('Size'),df

def compare(theory, real):
	t = (theory.drop('_spec_id', axis = 1).to_dict('records'))
	r = (real.drop('_spec_nb', axis = 1).to_dict('records'))
	d_t = [x for x in r if x not in t]
	print(len(d_t),'more specs have been calculated')
	d_r = [x for x in t if x not in r]
	print(len(d_r),'more specs have been missed')

def main() :
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A file with the correct format for the inventory')
	parser.add_argument("theory", help = 'A file with the correct format for the inventory')
	parser.add_argument("-t", "--time_data", default=_sys.stdout)
	parser.add_argument("-s", "--specs_data", default=_sys.stdout)
	args = parser.parse_args(_sys.argv[1:])
	file_name = args.inventory
	write_time = args.time_data
	write_specs = args.specs_data
	df, spec_frame = time_specs(file_name, write_time, write_specs)
	df.to_csv(write_time, mode = 'w', header=True, index=False)
	theory_frame = _dm.open_file(args.theory)
	compare(theory_frame, spec_frame)
	
		
if __name__ == "__main__":
	main()