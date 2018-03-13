import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import imbalance as ib
import mpairs as mp
import util as ut

invTest = pd.read_csv("aarInv.csv")
specTest = pd.read_csv("aarSpecs.csv")

who = invTest.loc[invTest['segment_type']=='Consonant']
spe0 = specTest.iloc[103].to_dict()
ut.clean(spe0)
nmp = mp.nmpairs(who, spe0)
print(nmp)

