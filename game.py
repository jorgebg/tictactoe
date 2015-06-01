from itertools import cycle

from .space import Token, Board
from .ui import Events, Console

UI = Console()

class State(Board):

    @property
    def empty_points(self):
        return [p for p, v in enumerate(self) if v is 0]

    @property
    def turn(self):
        return self.Length - len(self.empty_points)

    @property
    def token(self):
        return Round.Order[self.turn % len(Round.Order)]


    @property
    def winner(self):
        B = self
        lines = (
            B[:3], B[3:6], B[6:],       #horizontal
            B[::3], B[1::3], B[2::3],   #vertical
            B[::4], B[2:8:2]            #diagonal
        )
        for line in lines:
            for player in Round.Order:
                if line.count(player) is 3:
                    return player

    @property
    def is_over(self):
        return self.winner or not len(self.empty_points)

    def play(self, move):
        self[move] = self.token.value

    def next(self, move):
        state = State(self)
        state.play(move)
        return state


class Round(object):

    Order = [Token.X, Token.O]

    def __init__(self, X, O):
        """
        X and O must be instances of players.Player
        """
        self.state = State()
        self.players = { Token.X: X, Token.O: X }

    def run(self):
        s = self.state
        UI.update(Events.Start, {k.name: v for k,v in self.players.items()})
        while not s.is_over:
            token, turn = s.token, s.turn
            player = self.players[token]
            move = player.play(self.state)
            self.state = s = s.next(move)
            UI.update(Events.Move, locals())

        if s.winner is not None:
            token, player = s.winner, self.players[token]
            UI.update(Events.Win, locals())
        else:
            UI.update(Events.Draw)



class Tree(object):

    def __init__(self):
        self.states = set()
        self.unique_states = set()
        self.dict = dict()

    def generate(self):
        initial = State()
        self.states.add(initial)
        self.dict[initial] = self.children(initial)
        return self.dict

    def children(self, state=State()):
        if state.is_over:
            return dict()

        tree={}
        for move in state.empty_points:
            next_state = state.next(move)
            self.states.add(next_state)
            self.unique_states.add(State(next_state.min()))
            tree[next_state] = self.children(next_state)
        return tree

    def save(self):
        pass

    def load(self):
        pass
