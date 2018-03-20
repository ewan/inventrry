import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import imbalance as ib
import mpairs as mp
import stats as st
import util as ut

invTest = pd.read_csv("aarInv.csv")
specTest = pd.read_csv("aarSpecs.csv")
normTab = pd.read_feather("geoms.feather")

sType = ['Whole', 'Consonant','Stop/affricate', 'Vowel']

def script( sType, invTest, specTest, normTab ) : 
	mainDict = {}
	for t in sType :
		mainDict[t] = {'e' : [] , 'l' : [], 'g' : []}
		inv = invTest.loc[invTest['segment_type']==t]
		spe = specTest.loc[specTest['segment_type']==t]
		l = spe.shape[0] 
		for spec in range(l) : 
			e, l, g = st.stats(inv, (ut.getTrueSpecs(spe.iloc[spec].to_dict())),normTab)
			mainDict[t]['e'].append(e)
			mainDict[t]['l'].append(l)
			mainDict[t]['g'].append(g)
		for i in mainDict[t] :
			mainDict[t][i] = np.median(mainDict[t][i])
	return mainDict

test = script(sType, invTest, specTest, normTab)
'''
who = invTest.loc[invTest['segment_type']=='Stop/affricate']
spe = []
for i in range(145,150) :
	spe.append(ut.getTrueSpecs(specTest.iloc[i].to_dict()))
test = {'e' : [] , 'l' : [], 'g' : []}
for spec in spe : 
	e,l, g = st.stats(who, spec, normTab) 
	test['e'].append(e)
	test['l'].append(l)
	test['g'].append(g)

for i in test :
	print(np.median(test[i]))
'''