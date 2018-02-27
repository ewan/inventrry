import numpy as np
import pandas as pd
import sys
sys.path.append('../')
import imbalance
import util as ut

invTest = pd.read_csv("aarInv.csv")
specTest = pd.read_csv("aarSpecs.csv")

print(ut.binary_counts( invTest['high'] ))
k = ut.otn2( invTest['high'] )
print(k	)

print(ut.binary_counts( k))