from abc import ABCMeta, abstractmethod
from enum import Enum

from .space import Token, Board

class Events(Enum):
    Start = 0
    Move = 1
    Win = 2
    Draw = 3

class Base(metaclass=ABCMeta):

    @abstractmethod
    def update(self, event, data={}):
        """
        event must be a value of the enum .ui.Events
        """
        pass

    @abstractmethod
    def input_move(self):
        pass

class Console(Base):

    Templates = {
        Events.Start: 'Game started: {X} "X" vs {O} "O"',
        Events.Move: '{player} "{token.name}" chooses {move} [turn {turn}]',
        Events.Win: '{player} "{token.name}" wins',
        Events.Draw: 'draw'
    }

    def update(self, event, data={}):
        print(self.Templates[event].format(**data))

    def input_move(self, state):
        self.print_board(state)
        move, moves = None, state.empty_points
        while move not in moves:
            move = int(input("Enter a number {}: ".format(moves)))
        return move

    def print_board(self, state):
        points = Board.Points[::]
        for i, v in enumerate(state):
            token = Token(v)
            if token is not Token.Empty:
                points[i] = token.name
        board = zip(*[iter(points)]*3)
        for row in board:
            print(('{} '*3).format(*row))
