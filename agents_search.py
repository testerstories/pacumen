import sys
import time

import search
import utilities
from game.actions import Actions
from game.agent import Agent
from game.direction import Direction


##########
# AGENTS #
##########


class SearchAgent(Agent):
    """
    A general search agent that finds a path using a supplied search
    algorithm for a supplied search problem with a supplied heuristic.

    By default this agent runs a depth first search (algorithm) using
    a position search problem with a null heuristic.
    """
    def __init__(self, fn='depth_first_search', prob='PositionSearchProblem', heuristic='null_heuristic'):
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')

        func = getattr(search, fn)

        if sys.version_info >= (3, 0):
            functional = func.__code__.co_varnames
        else:
            functional = func.func_code.co_varnames

        if 'heuristic' not in functional:
            print('[SearchAgent] using function ' + fn)
            self.search_function = func
        else:
            if heuristic in globals().keys():
                heuristic_name = globals()[heuristic]
            elif heuristic in dir(search):
                heuristic_name = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in agents_search.py or search.py.')

            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            self.search_function = lambda x: func(x, heuristic=heuristic_name)

        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in agents_search.py.')

        self.search_type = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def register_initial_state(self, state):
        """
        Determine the layout of the game and, from that, choose a path to the
        goal. It's here that the agent should compute the path to the goal and
        store it in a local variable called `actions`.
        """
        if self.search_function is None:
            raise Exception("No search function provided for SearchAgent")

        start_time = time.time()

        problem = self.search_type(state)

        self.actions = self.search_function(problem)

        total_cost = problem.get_cost_of_actions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (total_cost, time.time() - start_time))

        if '_expanded' in dir(problem):
            print('Search nodes expanded: %d' % problem._expanded)

    def get_action(self, state):
        """
        Returns the next action in a chosen path. Will return Directions.STOP
        if there is no further action to take.
        """
        if 'action_index' not in dir(self):
            self.action_index = 0

        i = self.action_index
        self.action_index += 1

        if i < len(self.actions):
            return self.actions[i]
        else:
            return Direction.STOP


class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes the agent
    for being in positions on the west side of the board.
    """
    def __init__(self):
        self.search_function = search.uniform_cost_search
        cost_function = lambda pos: .5 ** pos[0]
        self.search_type = lambda state: PositionSearchProblem(state, cost_function, (1, 1), None, False)


class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes the agent
    for being in positions on the east side of the board.
    """
    def __init__(self):
        self.search_function = search.uniform_cost_search
        cost_function = lambda pos: 2 ** pos[0]
        self.search_type = lambda state: PositionSearchProblem(state, cost_function)


class AStarCornersAgent(SearchAgent):
    """
    A SearchAgent designed for the CornersProblem using A* search and
    a specific corners heuristic."
    """
    def __init__(self):
        self.search_function = lambda prob: search.astar_search(prob, corners_heuristic)
        self.search_type = CornersProblem


class AStarFoodSearchAgent(SearchAgent):
    """
    A SearchAgent designed to for the FoodSearchProblem using an A* search
    and a specific food heuristic.
    """
    def __init__(self):
        self.search_function = lambda prob: search.astar_search(prob, food_heuristic)
        self.search_type = FoodSearchProblem


class ClosestDotSearchAgent(SearchAgent):
    """
    An agent that will search for all food using a sequence of searches.
    """
    def register_initial_state(self, state):
        self.actions = []
        current_state = state

        while current_state.get_food().count() > 0:
            next_path_segment = self.find_path_to_closest_dot(current_state)
            self.actions += next_path_segment

            for action in next_path_segment:
                legal = current_state.get_legal_actions()
                if action not in legal:
                    t = (str(action), str(current_state))
                    raise Exception('find_path_closest_dot returned an illegal move: %s!\n%s' % t)

                current_state = current_state.generate_successor(0, action)
        self.action_index = 0

        print('Path found with cost %d.' % len(self.actions))

    def find_path_to_closest_dot(self, game_state):
        """
        Returns a path, composed of a list of actions, to the closest dot,
        starting from the current game state.
        """
        start_position = game_state.get_pacman_position()
        food = game_state.get_food()
        walls = game_state.get_walls()
        problem = AnyFoodSearchProblem(game_state)

        "*** YOUR CODE HERE ***"

        utilities.raise_not_defined()


##############
# HEURISTICS #
##############


def manhattan_heuristic(position, problem, info={}):
    """
    A heuristic that returns the Manhattan distance. The Manhattan distance
    refers to the distance between two points on a grid based on a strictly
    horizontal and/or vertical path, as opposed to the diagonal distance.
    """
    xy1 = position
    xy2 = problem.goal

    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclidean_heuristic(position, problem, info={}):
    """
    A heuristic that returns the Euclidean distance. The Euclidean distance
    refers to the the straight-line distance between two points in a grid.
    """
    xy1 = position
    xy2 = problem.goal

    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


def corners_heuristic(state, problem):
    """
    A heuristic for a CornersProblem. This heuristic function should always
    return a number that is a lower bound on the shortest path from the state
    to a goal of the problem. This means the heuristic should be admissible
    as well as consistent.
    """
    corners = problem.corners
    walls = problem.walls

    "*** YOUR CODE HERE ***"

    return 0


def food_heuristic(state, problem):
    """
    A heuristic for a FoodSearchProblem. This heuristic function should always
    return a number that is a lower bound on the shortest path from the state
    to a goal of the problem. This means the heuristic should be admissible
    as well as consistent.
    """
    position, food_grid = state

    "*** YOUR CODE HERE ***"

    return 0


############
# PROBLEMS #
############


class SearchProblem:
    """
    This class outlines the structure of a search problem. The methods here
    should only be implemented in classes that derive from this one.
    """
    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        utilities.raise_not_defined()

    def is_goal_state(self, state):
        """
        Returns true if and only if the state is a valid goal state.
        """
        utilities.raise_not_defined()

    def get_successors(self, state):
        """
        For a given state, this should return a list of triples, made up of
        (successor, action, step_cost).

        'successor' is a successor to the current state
        'action' is the action required to get to the successor
        'step_cost' is the incremental cost of expanding to that successor
        """
        utilities.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
        Returns the total cost of a particular sequence of actions. The
        sequence must be composed of legal moves.
        """
        utilities.raise_not_defined()


class PositionSearchProblem(SearchProblem):
    """
    This search problem can be used to find paths to a particular point
    on the pacman board.
    """
    def __init__(self, game_state, cost_function=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        self.walls = game_state.get_walls()
        self.start_state = game_state.get_pacman_position()

        if start is not None:
            self.start_state = start

        self.goal = goal
        self.cost_function = cost_function

        self.visualize = visualize
        if warn and (game_state.get_num_food() != 1 or not game_state.has_food(*goal)):
            print('Warning: this does not look like a regular search maze')

        self._visited, self._visited_list, self._expanded = {}, [], 0

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        is_goal = state == self.goal

        if is_goal and self.visualize:
            self._visited_list.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'draw_expanded_cells' in dir(__main__._display):
                    __main__._display.draw_expanded_cells(self._visited_list)

        return is_goal

    def get_successors(self, state):
        successors = []

        for action in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            x, y = state
            dx, dy = Actions.direction_to_vector(action)
            next_x, next_y = int(x + dx), int(y + dy)

            if not self.walls[next_x][next_y]:
                next_state = (next_x, next_y)
                cost = self.cost_function(next_state)
                successors.append((next_state, action, cost))

        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visited_list.append(state)

        return successors

    def get_cost_of_actions(self, actions):
        if actions is None:
            return 999999

        x, y = self.get_start_state()
        cost = 0

        for action in actions:
            dx, dy = Actions.direction_to_vector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999
            cost += self.cost_function((x, y))

        return cost


class CornersProblem(SearchProblem):
    """
    A search problem associated with finding paths through all four
    corners of a layout.
    """
    def __init__(self, starting_game_state):
        self.walls = starting_game_state.get_walls()
        self.starting_position = starting_game_state.get_pacman_position()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))

        for corner in self.corners:
            if not starting_game_state.has_food(*corner):
                print('Warning: no food in corner ' + str(corner))

        self._expanded = 0

        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        utilities.raise_not_defined()

    def is_goal_state(self, state):
        utilities.raise_not_defined()

    def get_successors(self, state):
        successors = []

        for action in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            "*** YOUR CODE HERE ***"

        self._expanded += 1
        return successors

    def get_cost_of_actions(self, actions):
        if actions is None:
            return 999999
        x, y = self.starting_position

        for action in actions:
            dx, dy = Actions.direction_to_vector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999

        return len(actions)


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of
    the food dots in a pacman game.
    """
    def __init__(self, starting_game_state):
        self.start = (starting_game_state.get_pacman_position(), starting_game_state.get_food())
        self.walls = starting_game_state.get_walls()
        self.starting_game_state = starting_game_state

        self._expanded = 0

        self.heuristic_info = {}

    def get_start_state(self):
        return self.start

    def is_goal_state(self, state):
        return state[1].count() == 0

    def get_successors(self, state):
        successors = []
        self._expanded += 1

        for direction in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            x,y = state[0]
            dx, dy = Actions.direction_to_vector(direction)
            next_x, next_y = int(x + dx), int(y + dy)

            if not self.walls[next_x][next_y]:
                next_food = state[1].copy()
                next_food[next_x][next_y] = False
                successors.append((((next_x, next_y), next_food), direction, 1))

        return successors

    def get_cost_of_actions(self, actions):
        x, y = self.get_start_state()[0]
        cost = 0

        for action in actions:
            dx, dy = Actions.direction_to_vector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999
            cost += 1

        return cost


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem associated with finding a path to any food.
    """
    def __init__(self, game_state):
        self.food = game_state.get_food()
        self.walls = game_state.get_walls()
        self.start_state = game_state.get_pacman_position()
        self.cost_function = lambda x: 1
        self._visited, self._visited_list, self._expanded = {}, [], 0

    def is_goal_state(self, state):
        x, y = state

        "*** YOUR CODE HERE ***"

        utilities.raise_not_defined()


def maze_distance(point1, point2, game_state):
    """
    Returns the maze distance between any two points, which can be used by
    any generic search function.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = game_state.get_walls()

    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)

    prob = PositionSearchProblem(game_state, start=point1, goal=point2, warn=False, visualize=False)

    return len(search.bfs(prob))
