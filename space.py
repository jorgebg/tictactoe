from enum import IntEnum

from . import ternary

class Token(IntEnum):
    _ = Empty = 0
    X = 1
    O = 2

class Board(ternary.Number):

    Points = list(range(3*3))
    Length = len(Points)
    Matrix = list(zip(*[iter(Points)]*3))
    Rotation = [point for row in zip(*Matrix[::-1]) for point in row]
    Inversion = list(map(int, [Token.Empty, Token.O, Token.X]))

    @classmethod
    def rotate(cls, x):
        return Board([x[i] for i in cls.Rotation])

    @classmethod
    def invert(cls, x):
        return Board([cls.Inversion[t] for t in x])

    @classmethod
    def mirror(cls, x):
        return Board(bytes(reversed(x)))

    def min(self, invert=True):
        board = self
        R, I, M = Board.rotate, Board.invert, Board.mirror
        if invert:
            functions = [R]*3 + [I] + [R]*3 + [M] + [R]*3 + [I] + [R]*3
        else:
            functions = [R]*3 + [M] + [R]*3
        y = [board]
        for f in functions:
            board = f(board)
            y.append(board)
        return Board(min(y))

    def __hash__(self):
        return self.int
