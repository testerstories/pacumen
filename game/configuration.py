from direction import Direction
from actions import Actions


class Configuration:
    """
    A Configuration instance holds the (x,y) coordinate of an agent, along
    with its traveling direction.

    The convention for positions, like a graph, is that (0,0) is the lower
    left corner, x increases horizontally and y increases vertically. This
    means north is the direction of increasing y, or (0,1).
    """

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def get_position(self):
        return self.pos

    def get_direction(self):
        return self.direction

    def is_integer(self):
        x, y = self.pos
        return x == int(x) and y == int(y)

    def __eq__(self, other):
        if other is None:
            return False

        return self.pos == other.pos and self.direction == other.direction

    def __hash__(self):
        x = hash(self.pos)
        y = hash(self.direction)
        return hash(x + 13 * y)

    def __str__(self):
        return "(x,y)=" + str(self.pos) + ", " + str(self.direction)

    def generate_successor(self, vector):
        """
        Generates a new configuration reached by translating the current
        configuration by the action vector.  This is a low-level call and does
        not attempt to respect the legality of the movement.

        Actions are movement vectors.
        """
        x, y = self.pos
        dx, dy = vector
        direction = Actions.vector_to_direction(vector)

        if direction == Direction.STOP:
            # There is no stop direction.
            direction = self.direction

        return Configuration((x + dx, y+dy), direction)
