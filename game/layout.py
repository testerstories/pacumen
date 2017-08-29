import os
import random
import logging

from .grid import Grid
from utilities import manhattan_distance

from functools import reduce

VISIBILITY_MATRIX_CACHE = {}


class Layout:
    def __init__(self, layout_text):
        self.width = len(layout_text[0])
        self.height = len(layout_text)
        self.walls = Grid(self.width, self.height, False)
        self.food = Grid(self.width, self.height, False)
        self.capsules = []
        self.agent_positions = []
        self.num_ghosts = 0
        self.process_layout_text(layout_text)
        self.layout_text = layout_text
        self.total_food = len(self.food.as_list())
        # self.initialize_visibility_matrix()

    def get_ghost_count(self):
        return self.num_ghosts

    # The concept of the visibility matrix was in place for a more refined
    # grid. The current approach simply uses boolean values for any aspect
    # of the grid. This is currently not being called but the functionality
    # may be revisited in the future.
    def initialize_visibility_matrix(self):
        global VISIBILITY_MATRIX_CACHE
        if reduce(str.__add__, self.layout_text) not in VISIBILITY_MATRIX_CACHE:
            from direction import Direction
            vectors = [(-0.5, 0), (0.5, 0), (0, -0.5), (0, 0.5)]
            dirs = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
            vis = Grid(self.width, self.height, {
                Direction.NORTH: set(),
                Direction.SOUTH: set(),
                Direction.EAST: set(),
                Direction.WEST: set(),
                Direction.STOP: set()
            })
            for x in range(self.width):
                for y in range(self.height):
                    if self.walls[x][y] is False:
                        for vector, direction in zip(vectors, dirs):
                            dx, dy = vector
                            next_x, next_y = x + dx, y + dy
                            while (next_x + next_y) != int(next_x) + int(next_y)\
                                    or not self.walls[int(next_x)][int(next_y)]:
                                vis[x][y][direction].add((next_x, next_y))
                                next_x, next_y = x + dx, y + dy
            self.visibility = vis
            VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layout_text)] = vis
        else:
            self.visibility = VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layout_text)]

    def is_wall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def get_random_legal_position(self):
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))

        while self.is_wall((x, y)):
            x = random.choice(range(self.width))
            y = random.choice(range(self.height))

        return x, y

    def get_random_corner(self):
        poses = [(1, 1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        return random.choice(poses)

    def get_furthest_corner(self, pacman_position):
        poses = [(1, 1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
        dist, pos = max([(manhattan_distance(p, pacman_position), p) for p in poses])
        return pos

    def is_visible_from(self, ghost_position, pacman_position, pacman_direction):
        row, col = [int(x) for x in pacman_position]
        return ghost_position in self.visibility[row][col][pacman_direction]

    def __str__(self):
        return "\n".join(self.layout_text)

    def deep_copy(self):
        return Layout(self.layout_text[:])

    def process_layout_text(self, layout_text):
        max_y = self.height - 1

        for y in range(self.height):
            for x in range(self.width):
                layout_char = layout_text[max_y - y][x]
                self.process_layout_character(x, y, layout_char)

        self.agent_positions.sort()
        self.agent_positions = [(i == 0, pos) for i, pos in self.agent_positions]

    def process_layout_character(self, x, y, layout_character):
        if layout_character == '%':
            self.walls[x][y] = True
        elif layout_character == '.':
            self.food[x][y] = True
        elif layout_character == 'o':
            self.capsules.append((x, y))
        elif layout_character == 'P':
            self.agent_positions.append((0, (x, y)))
        elif layout_character in ['G']:
            self.agent_positions.append((1, (x, y)))
            self.num_ghosts += 1
        elif layout_character in ['1', '2', '3', '4']:
            self.agent_positions.append((int(layout_character), (x, y)))
            self.num_ghosts += 1


def get_layout(name, back=2):
    if name.endswith('.lay'):
        layout = load_layout('layouts/' + name)
        if layout is None:
            layout = load_layout(name)
    else:
        layout = load_layout('layouts/' + name + '.lay')
        if layout is None:
            layout = load_layout(name + '.lay')

    if layout is None and back >= 0:
        current_directory = os.path.abspath('.')
        os.chdir('..')
        layout = get_layout(name, back - 1)
        os.chdir(current_directory)

    return layout


def load_layout(fullname):
    if not os.path.exists(fullname):
        return None

    f = open(fullname)

    try:
        return Layout([line.strip() for line in f])
    finally:
        f.close()
