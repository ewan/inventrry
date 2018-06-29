import pyinventrry.spec as _sp
import pyinventrry.data_manager as _dm
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

def time_specs(file_name, write_time, write_specs, verbose = False, force_csv = False) :	
	inventories, meta_keys, unique_list, feat_list = _sp.extract_from_file(file_name, force_csv)
	feat_dict = _sp.calculate_feat_dict(feat_list)
	feat_set = set(feat_dict)
	time_dict = {}
	df = _pd.DataFrame(columns=meta_keys + ['_spec_nb'] + feat_list)
	df.to_csv(write_specs, mode = 'w', header=True, index=False)
	
	time_frame = _pd.DataFrame(columns=['Size','Time'])
	time_frame.to_csv(write_time, mode = 'w', header=True, index=False)
	for unique in unique_list :
		df_phones = _dm.extract_data_frame(inventories, unique)
		phones = _sp.extract_phones(df_phones, feat_dict )
		
		wrapped = wrapper(_sp.calculate_one,feat_set,phones,feat_dict,df_phones)
		size = len(phones)
		
		time, specs = _ti.timeit(wrapped,setup ="gc.enable"  ,number =1)
		d = {'Size':size, 'Time' : time}
		time_frame = time_frame.append(d, ignore_index=True)
		time_frame.iloc[time_frame.shape[0]-1:].to_csv(write_time, mode = 'a', header=False, index=False)

		if size in time_dict :
			time_dict[size].append(time)
		else :
			time_dict[size] = [time]

		i = 1
		for spec in specs :
			d = dict(unique)
			d['_spec_id'] = 'Spec'+str(i)
			i+=1
			for feat in feat_list:
				d[feat] = False
			for t in spec:
				d[t] = True
			df = df.append(d, ignore_index=True)
		df.iloc[df.shape[0]-len(specs):df.shape[0]].to_csv(write_specs, mode = 'a', header=False, index=False)

	if verbose : 
		print('Specs dones')
		_sys.stdout.flush()

	time_frame = _pd.DataFrame(columns=['Size','Median','Variance'])
	
	for s in time_dict:
		d = {'Size' : s,'Median' :_np.median(time_dict[s]),'Variance' : _np.var(time_dict[s])}
		time_frame = time_frame.append(d, ignore_index=True)

	if verbose : 
		print('Median Time done')
		_sys.stdout.flush()
	
	return time_frame.sort_values('Size'),df, unique_list

def stringer(tab):
	s = ''
	for v in tab :
		if v :
			s+='T'
		else :
			s+='F'
	return s

def compare(theory, real, unique_list):
	theo = theory.drop('_spec_id', axis = 1)
	rea = real.drop('_spec_id', axis = 1)
	d_t = 0
	d_r = 0
	
	for unique in unique_list :
		t = _dm.extract_data_frame(theo, unique)
		r = _dm.extract_data_frame(rea, unique)
		t_t = set()
		t_r = set()
		for i in t.index :
			t_t.add(stringer(t.loc[i].to_dict().values()))
		for i in r.index :
			t_r.add(stringer(r.loc[i].to_dict().values()))

		d_t += len(t_r-t_t) 
		d_r += len(t_t-t_r) 
	
	print(d_t,'more specs have been calculated')
	_sys.stdout.flush()
	print(d_r,'more specs have been missed')
	_sys.stdout.flush()
	

def main() :
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory",
		help = 'A file with the correct format for the inventory')
	parser.add_argument("theory",
		help = 'The original spec file')
	parser.add_argument("-t", "--time_file", default=_sys.stdout,
		help = 'The path to where will be stored time calcule information')
	parser.add_argument("-s", "--specs_file", default=_sys.stdout,
		help = 'The path to where will be stored time calcule information')
	parser.add_argument("--verbose", action = 'store_true',
		help = '')
	parser.add_argument("-f", "--force_csv", action = 'store_true',
		help = 'Force the file to be considered as a csv')
	args = parser.parse_args(_sys.argv[1:])
	file_name = args.inventory
	write_time = args.time_file
	write_specs = args.specs_file
	time_frame, spec_frame, unique_list = time_specs(file_name, write_time, write_specs,
		args.verbose, args.force_csv)
	time_frame.to_csv(write_time, mode = 'w', header=True, index=False)
	theory_frame = _dm.open_file(args.theory)
	compare(theory_frame, spec_frame, unique_list)
	
		
if __name__ == "__main__":
	main()
