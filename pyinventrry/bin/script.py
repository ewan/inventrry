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
	meta = set()
	for k in all :
		if k=='' or k[0]=='_' :
			meta.add(k)
	metaV = {}
	for k in meta:
		metaV[k] = set(dataFrame[k].tolist())
	return meta,metaV

def tupleKeys(acc, wholeMeta, metaList):
	newAcc = []
	meta = metaList.pop()
	for t in acc : 
		for k in wholeMeta[meta] :
			l = list(t)
			l.append((meta,k))
			newAcc.append(l)
	if metaList : 
		return tupleKeys(newAcc, wholeMeta, metaList)
	else :
		return newAcc

def calculateScore( invTest, specTest, normTab ) : 
	metaKeys, wholeMeta = calculateMetaKeys(invTest)
	unique = tupleKeys([[]] , wholeMeta, list(metaKeys))
	
	mainDict = {}
	for t in unique:
		

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
	return mainDict

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
