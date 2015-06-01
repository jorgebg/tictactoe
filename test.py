import random
import unittest

from .game import Round, State, Tree
from .space import Board
from .players import *

class TestGame(unittest.TestCase):


    def test_board(self):
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

    if 0:
        ps = [Human(), Human()]
        ps = [Minimax(), Random()]
        #ps = [Net(), Random()]

        wins = dict.fromkeys(map(id, ps), 0)

        for i in range(100):
            r = Round(*ps)
            r.run()
            if r.state.winner is not None:
                wins[id(ps[r.state.winner])] += 1


        ps.reverse()
        for i in range(100):
            r = Round(*ps)
            r.run()
            if r.state.winner is not None:
                wins[id(ps[r.state.winner])] += 1

        for p in ps:
            print(p.name, wins[id(p)])


        #g.run([Minimax(), Human()])
