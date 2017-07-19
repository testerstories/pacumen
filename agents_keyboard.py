import random

from game.agent import Agent
from game.direction import Direction


class KeyboardAgent(Agent):
    """
    An agent controlled by the keyboard.
    """
    WEST_KEY = 'a'
    EAST_KEY = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__(self, index=0):
        self.lastMove = Direction.STOP
        self.index = index
        self.keys = []

    def get_action(self, state):
        from displays.graphical_board import keys_waiting
        from displays.graphical_board import keys_pressed

        keys = keys_waiting() + keys_pressed()

        if keys != []:
            self.keys = keys

        legal = state.get_legal_actions(self.index)
        move = self.get_move(legal)

        if move == Direction.STOP:
            # Try to move in the same direction as before.
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Direction.STOP in legal:
            move = Direction.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def get_move(self, legal):
        move = Direction.STOP

        if (self.WEST_KEY in self.keys or 'Left' in self.keys) and Direction.WEST in legal:
            move = Direction.WEST
        if (self.EAST_KEY in self.keys or 'Right' in self.keys) and Direction.EAST in legal:
            move = Direction.EAST
        if (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Direction.NORTH in legal:
            move = Direction.NORTH
        if (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Direction.SOUTH in legal:
            move = Direction.SOUTH

        return move


class KeyboardAgent2(KeyboardAgent):
    """
    A second agent controlled by the keyboard.
    """
    WEST_KEY = 'j'
    EAST_KEY = "l"
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'
    STOP_KEY = 'u'

    def get_move(self, legal):
        move = Direction.STOP

        if (self.WEST_KEY in self.keys) and Direction.WEST in legal:
            move = Direction.WEST
        if (self.EAST_KEY in self.keys) and Direction.EAST in legal:
            move = Direction.EAST
        if (self.NORTH_KEY in self.keys) and Direction.NORTH in legal:
            move = Direction.NORTH
        if (self.SOUTH_KEY in self.keys) and Direction.SOUTH in legal:
            move = Direction.SOUTH

        return move
