import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import imbalance as ib
import mpairs as mp
import util as ut

invTest = pd.read_csv("aarInv.csv")
specTest = pd.read_csv("aarSpecs.csv")

who = invTest.loc[invTest['segment_type']=='Whole']
spe0 = specTest.iloc[145].to_dict()
trueSpecs = ut.getTrueSpecs(spe0)