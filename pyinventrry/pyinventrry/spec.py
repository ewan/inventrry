import pandas as _pd
import sys as  _sys
import argparse
import pyinventrry.data_manager as _dm
import pyinventrry.prioList as _pl

def split_by(i, part, global_part):

	plus = []
	minus = []
	none = []
				
	for phon in part :
		if phon[i] == '+' or phon[i] == '1' or phon[i] == 1 or phon[i] == 'True' :
			plus.append(phon)
		elif phon[i] == '-' or phon[i] == '0' or phon[i] == 0 or phon[i] == 'False':
			minus.append(phon)
		else :
			none.append(phon)
				
	if ((len(part) == len(plus)) or (len(part) == len(minus)) or (len(part) == len(none))):
		global_part.append(part)
		return False
				
	else :
		if len(plus)>1 :
			global_part.append(plus)
		if len(minus)>1 :
			global_part.append(minus)
		if len(none) >1 :
			global_part.append(none)
		return True

def usefull_specs(feat_dict,phones) :

	parts = {}
	for i in feat_dict :
		gp = []
		split_by(i,phones,gp)
		parts[i]=gp
	pl = _pl.PrioList()
	for i in feat_dict : 
		if len(parts[i]) > 1 :
			x = abs(len(parts[i][0]) - len(parts[i][1]) )
			pl.put((x,i))
		else :
			pl.put((len(feat_dict),i))

	usefull = []
	while not pl.empty():
		usefull.append(pl.pop())

	return usefull

def calculate_spec(phones, feat_dict):

	partitionner = { () : [phones] }
	returN = []

	good_specs = usefull_specs(feat_dict,phones)

	for i in good_specs :
		to_add = {}
		for c in partitionner :
			global_part = []
			split = False
			for part in partitionner[c]:
				if split_by(i, part, global_part):
					split = True

			if split :
				tmp = list(c)
				tmp.append(i)
				tmp = tuple(tmp)
				w_part = partitionner[c]

				if global_part :
					to_add[tmp]=global_part
					pass

				else :
					returN.append(tmp)

		for add in to_add :
			partitionner[add]=to_add[add]

	return returN

def extract_from_file(file_name):
	df = _pd.read_csv(file_name)
	meta_keys = _dm.calculate_meta_keys(df)
	if not meta_keys :
		print('There is an error in the inventory file as no meta information was detected.',file=_sys.stderr)
		return 
	return df, meta_keys, _dm.calculate_unique(df,[[]], list(meta_keys)), _dm.calculate_normal_keys(df)

def calculate_feat_dict(features):
	feat_dict = {}
	i = 0
	for f in features :
		feat_dict[i]=f
		i+=1
	return feat_dict

def extract_phones(data_frame, feat_dict):
	tmp_phones = data_frame.to_dict('records')
	phones = []
	for p in tmp_phones :
		phon = []
		for f in range(len(feat_dict)):
			phon.append(p[feat_dict[f]])
		phones.append(phon)
	return phones
	
def calculate_all_specs(file_name):
	inventories, meta_keys, unique_list, feat_list = extract_from_file(file_name)
	feat_dict = calculate_feat_dict(feat_list)
	df = _pd.DataFrame(columns=meta_keys + ['_spec_nb'] + feat_list)
	for unique in unique_list :
		phones = extract_phones(_dm.extract_data_frame(inventories, unique), feat_dict )
		specs = calculate_spec(phones, feat_dict)
		i = 1
		for spec in specs :
			d = dict(unique)
			d['_spec_nb'] = 'Spec'+str(i)
			i+=1
			for feat in feat_list:
				d[feat] = 'False'
			for t in spec:
				d[feat_dict[t]] = 'True'
			df = df.append(d, ignore_index=True)
	
	return df

def ready_datas(file_name) :
	df = _pd.read_csv(file_name)
	
	features = df.columns.values.tolist()
	feat_dict = calculate_feat_dict(features)

	phones = extract_phones(df, feat_dict)

	return feat_dict,phones,len(feat_dict)

def turn_spec_number(feat_dict, feat_tuple):
	returN = []
	for i in feat_tuple:
		returN.append(feat_dict[i])
	return returN

def get_from_small(file_name):
	feat_dict,phones,i = ready_datas(file_name)
	specs = calculate_spec(phones,feat_dict)
	for u in specs :
		print(turn_spec_number(feat_dict, u))

def main() :
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A file with the correct format for the inventory')
	parser.add_argument("-w", "--write", default=_sys.stdout,)
	parser.add_argument("-s", "--small", action="store_true")
	args = parser.parse_args(_sys.argv[1:])
	file_name = args.inventory
	write_file = args.write
	if args.small :
		get_from_small(file_name)
	else :
		df = calculate_all_specs(file_name)
		df.to_csv(write_file, mode = 'w', header=True, index=False)

if __name__ == "__main__":
	main()