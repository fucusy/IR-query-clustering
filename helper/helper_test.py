__author__ = 'fucus'
import unittest
from helper import UF

class UFTest(unittest.TestCase):

    def test_init(self):
        uf = UF(10)
        self.assertEqual(uf.n, 10)
        self.assertEqual(uf.parent_data[9], 9)