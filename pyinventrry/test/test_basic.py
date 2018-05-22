# -*- encoding: utf-8 -*-
import pyinventrry as pi
import random as rd
import unittest
import pandas as pd
class scoreTest(unittest.TestCase):

	def setUp(self):
		self.inv = pd.read_csv('testInv.csv')
		self.spec = pd.read_csv('testSpec.csv')
		self.tspec = (pi.util.get_true_specs(self.spec))
	
	def test_econ_value(self):
		self.assertEqual(pi.score.ecovalue.econ_value(4,2), 1)
		self.assertNotEqual(pi.score.ecovalue.econ_value(4,2), 0)
	
	def test_mpairs(self):
		self.assertEqual(pi.score.mpairs.mpairs(self.inv, self.spec, 'f1'),2)
		self.assertNotEqual(pi.score.mpairs.mpairs(self.inv, self.spec, 'f2'),0)
		
	def test_n_mpairs(self):
		self.assertEqual(pi.score.mpairs.n_mpairs(self.inv, self.spec),6)
		self.assertNotEqual(pi.score.mpairs.n_mpairs(self.inv, self.spec),0)
		
	def test_imbalance(self):
		self.assertEqual(pi.score.imbalance.imbalance(pi.util.otn(self.inv.iloc[0])),1)
		self.assertNotEqual(pi.score.imbalance.imbalance(pi.util.otn(self.inv.iloc[0])),0)
		
	def test_n_imbalance(self):
		self.assertEqual(pi.score.imbalance.n_imbalance(self.inv, self.tspec),0)
		self.assertNotEqual(pi.score.imbalance.n_imbalance(self.inv, self.tspec),1)


unittest.main()