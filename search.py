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

class Point:
    def __init__(self, position, full_path, backward_cost):
        self.position = position
        self.full_path = full_path
        self.backward_cost = backward_cost


def null_heuristic(state, problem=None):
    return 0


def generic_search(problem, type, heuristic=null_heuristic):
    start_state = problem.get_start_state()
    start_point = Point(start_state, [], 0)
    is_visited = []

    if type == "DFS":
        points = utilities.Stack()
        points.push(start_point)
    elif type == "BFS":
        points = utilities.Queue()
        points.push(start_point)
    elif type == "UCS":
        points = utilities.PriorityQueue()
        points.push(start_point, 0)
    elif type == "A*":
        points = utilities.PriorityQueue()
        ch = heuristic(start_state, problem)
        points.push(start_point, ch)

    goal_point = ""
    found_goal = False

    while not points.is_empty():
        point = points.pop()

        if point.position in is_visited:
            continue

        is_visited.append(point.position)

        if problem.is_goal_state(point.position):
            goal_point = point
            found_goal = True
            break

        for neighbor in problem.get_successors(point.position):
            neighbor_position = neighbor[0]
            neighbor_direction = neighbor[1]
            neighbor_distance = neighbor[2]

            if neighbor_position not in is_visited:
                backward_cost = point.backward_cost + neighbor_distance
                full_path = point.full_path + [neighbor_direction]
                new_point = Point(neighbor_position, full_path, backward_cost)

                if type == "DFS" or type == "BFS":
                    points.push(new_point)

                if type == "UCS" or type == "A*":
                    if type == "UCS":
                        h = backward_cost
                    else:
                        h = heuristic(neighbor_position, problem) + backward_cost

                    points.push(new_point, h)

    if found_goal:
        return goal_point.full_path
    else:
        print("Unable to find the goal.")
        return []


def depth_first_search(problem):
    solution = generic_search(problem, "DFS")
    return solution


def breadth_first_search(problem):
    solution = generic_search(problem, "BFS")
    return solution


def uniform_cost_search(problem):
    solution = generic_search(problem, "UCS")
    return solution


def astar_search(problem, heuristic=null_heuristic):
    solution = generic_search(problem, "A*", heuristic)
    return solution


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = astar_search
ucs = uniform_cost_search
