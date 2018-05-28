import pandas as _pd
import sys as  _sys

def ready_datas(file_name) :
	df = _pd.read_csv(file_name)
	tmp_phones = df.to_dict('records')
	features = df.columns.values.tolist()
	
	feat_dict = {}
	i = 0
	for f in features :
		feat_dict[i]=f
		i+=1
	phones = []
	for p in tmp_phones :
		phon = []
		for f in range(i):
			phon.append(p[feat_dict[f]])
		phones.append(phon)

	return feat_dict,phones,i

def split_by(i, part, global_part):

	plus = []
	minus = []
	none = []
				
	for phon in part :
		if phon[i] == '+':
			plus.append(phon)
		elif phon[i] == '-':
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

def calculate_spec(phones, nb_specs, feat_dict):

	partitionner = { () : [phones] }
	returN = []

	for i in range(nb_specs) :
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
				if global_part :
					to_add[tmp]=global_part
					pass

				else :
					returN.append(tmp)

		for add in to_add :
			partitionner[add]=to_add[add]

	return returN

def turn_spec_number(feat_dict, feat_tuple):
	returN = []
	for i in feat_tuple:
		returN.append(feat_dict[i])
	return returN

def main() :
	file_name = _sys.argv[1]
	feat_dict,phones,i = ready_datas(file_name)
	specs = calculate_spec(phones,i, feat_dict)

	for u in specs :
		print(turn_spec_number(feat_dict, u))

if __name__ == "__main__":
	main()




