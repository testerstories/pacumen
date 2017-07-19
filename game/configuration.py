from .direction import Direction
from .actions import Actions


class Configuration:
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
        x, y = self.pos
        dx, dy = vector
        direction = Actions.vector_to_direction(vector)

        if direction == Direction.STOP:
            direction = self.direction

        return Configuration((x + dx, y+dy), direction)
