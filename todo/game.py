
import random

from enum import Enum

X, O = TOKENS = 'XO'

WIN_MASKS = [
    0b100100100,
    0b10010010,
    0b1001001,
    0b111000000,
    0b111000,
    0b111,
    0b100010001,
    0b1010100,
]

SIZE = 9
EMPTY = 2 ** SIZE - 1
FULL = 0


Events = Enum('Events', 'Start Move Win Draw')

class Tree:
  pass


class State:

  def __init__(self, board=0, space=EMPTY):
    self.board = board
    self.space = space

  def next(self, move):
    i = 2**(move-1)
    # space = self.space ^ i
    # board = self.board
    # if self.token is O:
    #   board |= i
    space = self.space ^ i
    board = ((self.board | i) ^ EMPTY) ^ space
    return State(board, space)

  @property
  def id(self):
    raise NotImplemented

  @property
  def token(self):
    return TOKENS[1-len(self.moves)%2]

  @property
  def finished(self):
    return self.winner or self.space is FULL

  @property
  def winner(self):
    # sides = {
    #     X: (self.board ^ EMPTY) ^ self.space,
    #     O: self.board
    # }
    # for token, board in sides.items():
      for mask in WIN_MASKS:
        # if (board & mask) == mask:
        if (self.board & mask) == mask:
          return token

  @property
  def moves(self):
    return [i + 1 for i in range(SIZE) if self.space & 2**i]

  @property
  def turn(self):
    return SIZE-len(self.moves)

  def __repr__(self):
    points = []
    for i in range(SIZE):
      point = str(i + 1)
      if not self.space & 2 ** i:
        point = TOKENS[bool(self.board & 2 ** i)]
      points.append(' ' + point)
      if i % 3 is 2:
        points.append("\n")
    return "".join(points)


class Game:

  def __init__(self, players, state=None, ui=None):
    self.players = {X: players[0](self), O: players[1](self)}
    self.state = state or State()
    self.ui = ui or Console()

  def run(self):
    self.ui.update(Events.Start, self.players)
    while not self.state.finished:
      token = self.state.token
      print(token, bin(self.state.space), bin(self.state.board))
      player = self.players[token]
      move = player.play()
      self.state = self.state.next(move)
      turn = self.state.turn
      self.ui.update(Events.Move, locals())

    if self.state.winner is None:
        self.ui.update(Events.Draw)
    else:
      token = self.state.winner
      player = self.players[token]
      self.ui.update(Events.Win, locals())

class Console:

  Templates = {
      Events.Start: 'Game started: {X} "X" vs {O} "O"',
      Events.Move: '{player} "{token}" chooses {move} [turn {turn}]',
      Events.Win: '{player} "{token}" wins',
      Events.Draw: 'draw'
  }

  def update(self, event, data={}):
    print(self.Templates[event].format(**data))

  def input_move(self, state):
    move, moves = None, state.moves
    while move not in moves:
      move = int(input("Enter a number {}: ".format(moves)))
    return move

  def show_state(self, state):
    print(state)


class Player:

  def __init__(self, game):
    self.game = game

  def play(self):
    raise NotImplemented

  def __repr__(self):
    return self.__class__.__name__


class Human(Player):

  def play(self):
    ui, state = self.game.ui, self.game.state
    ui.show_state(state)
    return ui.input_move(state)


class Random(Player):

  def play(self):
    return random.choice(self.game.state.moves)


g = Game([Random, Human])
g.run()

# g = State(0b110101100, 0)
# print(g)
# print(g.winner)
#
# print()
#
# g = State(0b010101001, 0)
# print(g)
# print(g.winner)
#
# print()
#
# g = State(0b010101001, 0b1)
# print(g)
# print(g.winner)
