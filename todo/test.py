import random
import unittest

from game import *

class TestGame(unittest.TestCase):


    def test_winner(self):
        wins = 
        """
        XOX
        XXO
        XOO

        XXX
        OXO
        OOX

        XOX
        XXO
        OOO
        """

        b0, b1, b2, b3 = Board("001001001"), Board("000000111"), Board("000000222"), Board(0)

        self.assertEqual(b0.min(), b1.min())
        self.assertEqual(b1.min(), b2.min())
        self.assertNotEqual(b1.min(False), b3.min(False))
        self.assertNotEqual(b2.min(), b3.min())

        tree = Tree()
        tree.generate()
        self.assertEqual(len(tree.states), 5478)
        #self.assertEqual(len(tree.unique_states), 765)
        #self.assertEqual(len([s for s in tree.unique_states if s.is_over]), 765)


if __name__ == '__main__':
    unittest.main()
