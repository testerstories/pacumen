import utilities


class SearchProblem:
    def get_start_state(self):
        utilities.raise_not_defined()

    def is_goal_state(self, state):
        utilities.raise_not_defined()

    def get_successors(self, state):
        utilities.raise_not_defined()

    def get_cost_of_actions(self, actions):
        utilities.raise_not_defined()


def depth_first_search(problem):
    utilities.raise_not_defined()


def breadth_first_search(problem):
    utilities.raise_not_defined()


def uniform_cost_search(problem):
    utilities.raise_not_defined()


def null_heuristic(state, problem=None):
    return 0


def astar_search(problem, heuristic=null_heuristic):
    utilities.raise_not_defined()


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = astar_search
ucs = uniform_cost_search
