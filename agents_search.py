import sys
import time

import search
import utilities
from game.actions import Actions
from game.agent import Agent
from game.direction import Direction


class SearchAgent(Agent):
    def __init__(self, fn='depth_first_search', prob='PositionSearchProblem', heuristic='null_heuristic'):
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')

        func = getattr(search, fn)

        if sys.version_info >= (3,0):
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
        if 'action_index' not in dir(self):
            self.action_index = 0

        i = self.action_index
        self.action_index += 1

        if i < len(self.actions):
            return self.actions[i]
        else:
            return Direction.STOP


class PositionSearchProblem(search.SearchProblem):
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

        # For display purposes; do not change.
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def get_start_state(self):
        return self.start_state

    def is_goal_state(self, state):
        is_goal = state == self.goal

        # For display purposes only; do not change.
        if is_goal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):
                    __main__._display.drawExpandedCells(self._visitedlist)

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

        # Bookkeeping for display purposes; do not change.
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def get_cost_of_actions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return an absurdly large number.
        """
        if actions is None:
            return 999999

        x,y= self.get_start_state()
        cost = 0

        for action in actions:
            # Figure out the next state and see whether its legal.
            dx, dy = Actions.direction_to_vector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999
            cost += self.cost_function((x, y))

        return cost


class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.search_function = search.uniform_cost_search
        cost_function = lambda pos: .5 ** pos[0]
        self.search_type = lambda state: PositionSearchProblem(state, cost_function, (1, 1), None, False)


class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.search_function = search.uniform_cost_search
        cost_function = lambda pos: 2 ** pos[0]
        self.search_type = lambda state: PositionSearchProblem(state, cost_function)


def manhattan_heuristic(position, problem, info={}):
    """
    The Manhattan distance heuristic for a PositionSearchProblem.
    """
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclidean_heuristic(position, problem, info={}):
    """
    The Euclidean distance heuristic for a PositionSearchProblem.
    """
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


#####################################################
# This portion is incomplete.  Time to write code.  #
#####################################################


class CornersProblem(search.SearchProblem):
    def __init__(self, starting_game_state):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = starting_game_state.get_walls()
        self.starting_position = starting_game_state.get_pacman_position()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))

        for corner in self.corners:
            if not starting_game_state.has_food(*corner):
                print('Warning: no food in corner ' + str(corner))

        # DO NOT CHANGE; Number of search nodes expanded.
        self._expanded = 0

        # Please add any code here which you would like to use
        # in initializing the problem.
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        "*** YOUR CODE HERE ***"
        utilities.raise_not_defined()

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        utilities.raise_not_defined()

    def get_successors(self, state):
        successors = []

        for action in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            # Add a successor state to the successor list if the action is legal.
            # Here's a code snippet for figuring out whether a new position hits
            # a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.direction_to_vector(action)
            #   next_x, next_y = int(x + dx), int(y + dy)
            #   hits_wall = self.walls[next_x][next_y]
            "*** YOUR CODE HERE ***"

        # Do not change this.
        self._expanded += 1
        return successors

    def get_cost_of_actions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999. This is implemented for you.
        """
        if actions is None:
            return 999999
        x, y = self.starting_position

        for action in actions:
            dx, dy = Actions.direction_to_vector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999

        return len(actions)


def corners_heuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e. it should be
    admissible (as well as consistent).
    """
    # These are the corner coordinates.
    corners = problem.corners

    # These are the walls of the maze, as a Grid.
    walls = problem.walls

    "*** YOUR CODE HERE ***"
    # Default to trivial solution.
    return 0


class AStarCornersAgent(SearchAgent):
    """
    A SearchAgent for the FoodSearchProblem using A* and your food_heuristic.
    """
    def __init__(self):
        self.search_function = lambda prob: search.astar_search(prob, corners_heuristic)
        self.search_type = CornersProblem


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple (pacman_position, food_grid) where
      pacman_position: a tuple (x,y) of integers specifying Pacman's position
      food_grid:       a Grid of either True or False, specifying remaining food
    """
    def __init__(self, starting_game_state):
        self.start = (starting_game_state.get_pacman_position(), starting_game_state.get_food())
        self.walls = starting_game_state.get_walls()
        self.startingGameState = starting_game_state

        # DO NOT CHANGE.
        self._expanded = 0

        # A dictionary for the heuristic to store information.
        self.heuristicInfo = {}

    def get_start_state(self):
        return self.start

    def is_goal_state(self, state):
        return state[1].count() == 0

    def get_successors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """
        successors = []
        # DO NOT CHANGE.
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
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        """
        x,y = self.get_start_state()[0]
        cost = 0

        for action in actions:
            # Figure out the next state and see whether it's legal.
            dx, dy = Actions.direction_to_vector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999
            cost += 1

        return cost


class AStarFoodSearchAgent(SearchAgent):
    """
    A SearchAgent for FoodSearchProblem using A* and your food_heuristic.
    """
    def __init__(self):
        self.search_function = lambda prob: search.astar_search(prob, food_heuristic)
        self.search_type = FoodSearchProblem


def food_heuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness. First, try to
    come up with an admissible heuristic; almost all admissible heuristics
    will be consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to
    get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, food_grid = state
    "*** YOUR CODE HERE ***"
    return 0


class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """
    def register_initial_state(self, state):
        self.actions = []
        current_state = state

        while current_state.get_food().count() > 0:
            # The missing piece
            next_path_segment = self.find_path_to_closest_dot(current_state)
            self.actions += next_path_segment

            for action in next_path_segment:
                legal = current_state.get_legal_actions()
                if action not in legal:
                    t = (str(action), str(current_state))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)

                current_state = current_state.generate_successor(0, action)
        self.action_index = 0

        print('Path found with cost %d.' % len(self.actions))

    def find_path_to_closest_dot(self, game_state):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        game state.
        """
        # Here are some useful elements of the start_state.
        start_position = game_state.get_pacman_position()
        food = game_state.get_food()
        walls = game_state.get_walls()
        problem = AnyFoodSearchProblem(game_state)

        "*** YOUR CODE HERE ***"
        utilities.raise_not_defined()


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below. The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in details for the
    find_path_to_closest_dot method.
    """

    def __init__(self, game_state):
        """
        Stores information from the game state. You don't need to change this.
        """
        # Store the food for later reference.
        self.food = game_state.get_food()

        # Store info for the PositionSearchProblem (no need to change this).
        self.walls = game_state.get_walls()
        self.start_state = game_state.get_pacman_position()
        self.cost_function = lambda x: 1
        # For display purposes; do not change.
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def is_goal_state(self, state):
        """
        The state is pacman's position. You would fill this in with a goal
        test that will complete the problem definition.
        """
        x, y = state

        "*** YOUR CODE HERE ***"
        utilities.raise_not_defined()


def maze_distance(point1, point2, game_state):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The game state can be any game state -- pacman's
    position in that state is ignored.

    Example usage: maze_distance( (2,4), (5,6), game_state)

    This might be a useful helper function for an ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = game_state.get_walls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(game_state, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
