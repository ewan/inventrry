import pandas as _pd
import sys as  _sys
import argparse
import pyinventrry.data_manager as _dm

def split_by(feat, part, global_part):

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
	b = False
	sPart = []
	for p in s :
		sPart.append(len(p))
	print(sPart)
	tPart = []
	for p in t :
		tPart.append(len(p))
	print(tPart)
	print('--------')
	t = list(t) 
	try:
		for elem in s:
			t.remove(elem)
	except (ValueError, TypeError) as e:
		b =  False
	if not b :
		return False
	b = not t
	return b

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

def tree_theory(phones, feat_set):
	top = Node(p = None, s = None, o = set(feat_set), pa = phones, n = {})
	top.generate()
	return top.get_specs(acc = [], actual = [])

def data_frame_theory(feat_set, phones, deep):
	specs = []
	for f in feat_set :
		done = True
		tmp = set(feat_set)
		tmp.remove(f)
		rmv = phones.loc[:,tmp].drop_duplicates()
		if rmv.shape[0] == 2:

			specs.append([f])

		if rmv.shape[0] != phones.shape[0]:
			done = False
			part = data_frame_theory(tmp, rmv, deep +1 )
			for s in part:
				s.append(f)
				specs.append(s)
		if (pow(2, deep)>= rmv.shape[0]):
			specs.append([f])
	return specs



	input('Be ready for ^C')

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
	feat_set = set(feat_dict)
	df = _pd.DataFrame(columns=meta_keys + ['_spec_nb'] + feat_list)
	for unique in unique_list :
		phones = extract_phones(_dm.extract_data_frame(inventories, unique), feat_dict )
		phones = _dm.extract_data_frame(inventories, unique)
		specs = data_frame_theory(feat_list, phones, 0)
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