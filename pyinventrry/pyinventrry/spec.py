import pandas as _pd
import sys as  _sys
import argparse
import pyinventrry.data_manager as _dm

def splitter(feat, part):
	plus = []
	minus = []
	none = []
	for phon in part :
		if phon[feat] == '+' or phon[feat] == '1' or phon[feat] == 1 or phon[feat] == 'True' :
			plus.append(phon)
		elif phon[feat] == '-' or phon[feat] == '0' or phon[feat] == 0 or phon[feat] == 'False':
			minus.append(phon)
		else :
			none.append(phon)

	return plus, minus, none	

def split_by(feat, part, global_part):

	plus, minus, none = splitter(feat, part)
				
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

def compare(s, t):
	# Is s better than t 
	
	t = list(t)   # make a mutable copy
	try:
		for elem in s:
			t.remove(elem)
	except (ValueError, TypeError) as e:
		return False
	return not t

class Node:

	def __init__(self,p, s, o, pa, n, e = False): 
		self.parent = p
		self.splitter = s
		self.other = o
		self.parts = pa
		self.next = n
		self.end = e

	def better(self, parts, feat):
		if self.parent is None :
			return False
		return compare(self.parent.next[feat].parts, parts)

	def generate(self):
		if self.end:
			return 

		to_add = {}
		to_end = set()
		for i in self.other :
			g = []
			split = False
			for p in self.parts :
				if split_by(i, p, g):
					split = True
			if split :
				if self.parent is not None :
					if self.splitter in self.parent.next[i].other :
						self.parent.next[i].other.remove(self.splitter)
				if self.better(g,i):
					to_end.add(i)
				else :
					if g :
						to_add[i] = g
					else :
						self.next[i] = Node( p = self, s = i, o = {}, pa = [], n = {},  e = True)
		
		for i in to_end :
			self.other.remove(i)

		for i in to_add :
			other_feats = set(self.other)
			other_feats.remove(i)
			self.next[i] = Node( p = self, s = i, o = other_feats, pa = to_add[i], n = {})

		for n in self.next :
			self.next[n].generate()

	def get_specs(self, acc, actual) :
		if self.splitter == None :
			for n in self.next :
				self.next[n].get_specs(acc, [])
			return acc
		else :
			actual.append(self.splitter)
			if self.end :
				acc.append(actual)
			else :
				for n in self.next:
					self.next[n].get_specs( acc, list(actual))
			return 

def tree_theory(feat_set, phones):
	top = Node(p = None, s = None, o = set(feat_set), pa = phones, n = {})
	top.generate()
	return top.get_specs(acc = [], actual = [])

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
	
def check_spec(spec, phones):
	b = True
	for feat in spec:
		s = set(spec)
		s.remove(feat)
		b = b and phones.loc[:,s].drop_duplicates().shape[0] != phones.loc[:,spec].drop_duplicates().shape[0]

	return b

def calculate_all_specs(file_name):
	inventories, meta_keys, unique_list, feat_list = extract_from_file(file_name)
	feat_dict = calculate_feat_dict(feat_list)
	feat_set = set(feat_dict)
	df = _pd.DataFrame(columns=meta_keys + ['_spec_nb'] + feat_list)
	for unique in unique_list :
		df_phones = phones = _dm.extract_data_frame(inventories, unique)
		
		phones = extract_phones(df_phones, feat_dict )
		int_specs = tree_theory(feat_set, [phones])
		
		specs = []
		for int_spec in int_specs :
			spec = set()
			for i in int_spec:
				spec.add(feat_dict[i])
			if check_spec(spec, df_phones):
				specs.append(spec)

		i = 1
		for spec in specs :
			d = dict(unique)
			d['_spec_nb'] = 'Spec'+str(i)
			i+=1
			for feat in feat_list:
				d[feat] = 'False'
			for t in spec:
				d[t] = 'True'
			df = df.append(d, ignore_index=True)
	return df

def main() :
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A file with the correct format for the inventory')
	parser.add_argument("-w", "--write", default=_sys.stdout,)
	args = parser.parse_args(_sys.argv[1:])
	file_name = args.inventory
	write_file = args.write
	df = calculate_all_specs(file_name)
	df.to_csv(write_file, mode = 'w', header=True, index=False)

if __name__ == "__main__":
	main()