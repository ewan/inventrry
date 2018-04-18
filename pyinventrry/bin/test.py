import pandas as pd
inv = pd.read_csv("../datasTest/aarInv.csv")
spec = pd.read_csv("../datasTest/aarSpecs.csv")
tab = pd.read_feather("../datasTest/geoms.feather")
import script
script.calculateScore(inv,spec,tab)