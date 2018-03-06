import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import imbalance as ib
import util as ut

invTest = pd.read_csv("aarInv.csv")
specTest = pd.read_csv("aarSpecs.csv")

who = invTest.loc[invTest['segment_type']=='Whole']
spe0 = specTest.iloc[0]

nimb = ib.nimbalance(who, spe0)
print(nimb)