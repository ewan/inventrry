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
	language = set(specTest['language'].values)
	mainDict = {}
	for lang in language :
		mainDict[lang]={}
		for t in sType :
			mainDict[lang][t] = {'Econ' : [] , 'Loc' : [], 'Glob' : []}
			inv = invTest.loc[(invTest['segment_type']==t) & (invTest['language']==lang)]
			spe = specTest.loc[(specTest['segment_type']==t) & (specTest['language']==lang)]
			leng = spe.shape[0] 
			for spec in range(leng) : 
				e, l, g = st.stats(inv, (ut.getTrueSpecs(spe.iloc[spec].to_dict())),normTab)
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
	
dict = script(sType, invTest, specTest, normTab)

test = generateDataFrame(dict)
test.to_csv('aarScore.csv')
