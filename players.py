import os
import shelve
import random
from abc import ABCMeta, abstractmethod

from .game import State, Token, UI

class Player(metaclass=ABCMeta):

    @property
    def name(self):
        return type(self).__name__

    @abstractmethod
    def play(self, state):
        pass

    def __str__(self):
        return self.name

class Human(Player):
    def play(self, state):
        return UI.input_move(state)


class Robot(Player):

    persist = True

    def __init__(self):
        super(Robot, self).__init__()
        if self.persist:
            self.load()

    @property
    def filename(self):
        return ".data/" + self.name + ".p"

    def load(self, flag='r'):
        file = self.filename
        os.makedirs(os.dirname(file))
        self.data = shelve.open(file, flag=flag, writeback=True)

    def train(self):
        self.data.close()
        self.load('n')
        self.fit()
        self.data.close()
        self.load()

    def fit(self):
        return NotImplemented


class Random(Robot):
    persist = False
    def play(self, state):
        return random.choice(state.empty_points)


class Minimax(Robot):
    def play(self, state):
        return self.data[state]

    def score(self, state, depth):
        if state.winner is Token.X:
            return 10 - depth
        elif state.winner is Token.O:
            return depth - 10
        else:
            return 0

    """
    minimax algorithm
    """
    def fit(self, state=State(), depth=0):
        if state.is_over:
            return self.score(state, depth)

        moves = state.empty_points
        scores = [self.fit(state.next(m), depth+1) for m in moves]

        if state.token is Token.X:
            s = max(scores)
        else:
            s = min(scores)

        i = scores.index(s)
        print(len(self.data.keys()))
        self.data[state] = moves[i]
        return scores[i]

class Net(Robot):
    def train(self):
        data = {self.normalize(i): [o] for i, o in Minimax().data.items()}
        from . import net
        n = net.Net(9, 9, 1)
        n.train(data, 5, 1, 0.5)
        self.data = n

    def normalize(self, i):
        i = tuple(map(int,i) + [-1]*(9 - len(i)))
        return i

    def play(self, state):
        i = self.normalize(state.serialize())
        o = int(round((self.data.test(i)[0])))
        if o not in state.empty_points:
            raise ValueError(o)
        return o

class BigNet(Robot):
    def train(self):
        data = {tuple(map(int, k.ljust(9, '0'))): self.decode(v) for k, v in Minimax().data.items()}
        from . import net
        n = net.Net(9, 9, 9)
        n.train(data)
        self.data = n

    def encode(self, output):
        return output.index(max(output));

    def decode(self, output):
        x = [0]*9
        x[output] = 1
        return x

    def play(self, state):
        return self.encode(self.data.test(state))
