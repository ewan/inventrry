#!/usr/bin/env python

import numpy as np
import sys
import argparse
import pandas as pd
import pyinventrry as pi
import pyinventrry.util as ut

sType = ['Whole', 'Consonant','Stop/affricate', 'Vowel']

def calculateMetaKeys(dataFrame):
	all = [ x for x in dataFrame ]
	meta = []
	for k in all :
		if k=='' or k[0]=='_' :
			meta.append(k)
	return meta

def calculateUnique(dataframe, acc, meta):
	newAcc = []
	mKey = meta.pop()
	tmp = pd.DataFrame(dataframe)
	for k in acc :
		for tk in k :
			tmp = tmp.loc[tmp[tk[0]]==tk[1]]
		uni = tmp[mKey].unique()
		for n in uni :
			newKey = list(k)
			newKey.append((mKey,n))
			newAcc.append(newKey)
	if meta :
		return calculateUnique(dataframe, newAcc, meta)
	else :
		return newAcc

def extractDataFrame(DataFrame, tuples):
	ret = pd.DataFrame(DataFrame)
	for t in tuples :
		ret = ret.loc[ret[t[0]]==t[1]]
		ret.drop(t[0],axis=1)
	return ret

def calculateScore( invTest, specTest, normTab ) : 
	metaKeys = calculateMetaKeys(invTest)
	unique = calculateUnique(invTest,[[]], list(metaKeys))
	'''
	OK here
	'''
	result = pd.DataFrame(columns=metaKeys+['econ','loc','glob'])
	for t in unique:
	
		inv = extractDataFrame(invTest, t)
		spe = extractDataFrame(specTest, t)
		leng = spe.shape[0] 
		for spec in range(leng) : 
			e, l, g = pi.stats.stat(inv, (ut.getTrueSpecs(spe.iloc[spec].to_dict())),normTab)
			print(e,l,g)
		pass

	'''
	for lang in language :
		mainDict[lang]={}
		for t in sType :
			mainDict[lang][t] = {'Econ' : [] , 'Loc' : [], 'Glob' : []}
			inv = invTest.loc[(invTest['segment_type']==t) & (invTest['language']==lang)]
			spe = specTest.loc[(specTest['segment_type']==t) & (specTest['language']==lang)]
			leng = spe.shape[0] 
			for spec in range(leng) : 
				e, l, g = pi.stats(inv, (ut.getTrueSpecs(spe.iloc[spec].to_dict())),normTab)
				mainDict[lang][t]['Econ'].append(e)
				mainDict[lang][t]['Loc'].append(l)
				mainDict[lang][t]['Glob'].append(g)
			for i in mainDict[lang][t] :
				mainDict[lang][t][i] = np.nanmedian(mainDict[lang][t][i])
	'''
	return result

def generateDataFrame(dict):
	ret = pd.DataFrame(columns = ['Language','Type','Econ','Loc','Glob'])
	for l in dict :
		for t in dict[l]:
			master = {'Language' : l, 'Type' : t}
			all = {**master,**dict[l][t]}
			ret = ret.append(all, ignore_index=True)
	ret = ret[['Language','Type','Econ','Loc','Glob']]
	return ret

def writeScore(dict, filename) : 
	(generateDataFrame(dict)).to_csv(filename)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A csv file with the correct format for the inventory')
	parser.add_argument("specs", help = 'A csv file with the correct format for the specs')
	parser.add_argument("normTab", help = 'A file used for normalize data (actually in feather format)')
	#parser.add_argument('--max-cost', type=float,
	#					default=float("inf"))
	#parser.add_argument('--seed', type=int, default=None)
	#parser.add_argument('inventory_fn',
	#					help='csv containing features for a single inventory,'
	#					' with header, coded numerically')
	args = parser.parse_args(sys.argv[1:])
	dict = calculateScore(	sType,
				pd.read_csv(parser.inventory),
				pd.read_csv(parser.specs), 
				pd.read_feather(parser.normTab) )
	print(dict)
