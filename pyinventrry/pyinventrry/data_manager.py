import pandas as pd

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

def calculate_normal_keys(data_frame):
	'''
	Find all colummns name which don't start with an underscore
	:param data_frame: the DataFrame to analyse.
	:type data_frame: DataFrame
	:return: the list of all meta keys of the DataFrame
	:rtype: string array
	'''
	all = [ x for x in data_frame ]
	meta = []
	for k in all :
		if not (k=='' or k[0]=='_') :
			meta.append(k)
	return meta

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