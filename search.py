"""
In search.py, you will implement generic search algorithms which are called
by Pac-Man agents (in agents_search.py).
"""

import utilities


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't
    implement any of the methods.

    You do not ever need to change anything in this class.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        utilities.raise_not_defined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        utilities.raise_not_defined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost'
        is the incremental cost of expanding to that successor.
        """
        utilities.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        utilities.raise_not_defined()


def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tinyMaze. For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game.direction import Direction
    s = Direction.SOUTH
    w = Direction.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.get_start_state()
    print "Is the start a goal?", problem.is_goal_state(problem.get_start_state())
    print "Start's successors:", problem.get_successors(problem.get_start_state())
    """
    "*** YOUR CODE HERE ***"
    utilities.raise_not_defined()


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    utilities.raise_not_defined()


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    utilities.raise_not_defined()


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest goal in the provided SearchProblem. This heuristic is trivial.
    """
    return 0


def astar_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    utilities.raise_not_defined()


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = astar_search
ucs = uniform_cost_search
