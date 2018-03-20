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