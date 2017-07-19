from .configuration import Configuration
from .agent_state import AgentState
from .grid import reconstitute_grid, Grid
from .direction import Direction
from utilities import nearest_point


class GameStateData:
    def __init__(self, previous_state=None):
        if previous_state is not None:
            self.food = previous_state.food.shallow_copy()
            self.capsules = previous_state.capsules[:]
            self.agent_states = self.copy_agent_states(previous_state.agent_states)
            self.layout = previous_state.layout
            self._eaten = previous_state._eaten
            self.score = previous_state.score

        self._food_eaten = None
        self._food_added = None
        self._capsule_eaten = None
        self._agent_moved = None
        self._lose = False
        self._win = False
        self.score_change = 0

    def deep_copy(self):
        state = GameStateData(self)
        state.food = self.food.deep_copy()
        state.layout = self.layout.deep_copy()
        state._agent_moved = self._agent_moved
        state._food_eaten = self._food_eaten
        state._food_added = self._food_added
        state._capsule_eaten = self._capsule_eaten
        return state

    @staticmethod
    def copy_agent_states(agent_states):
        copied_states = []

        for agentState in agent_states:
            copied_states.append(agentState.copy())

        return copied_states

    def __eq__(self, other):
        if other is None:
            return False

        if not self.agent_states == other.agent_states:
            return False
        if not self.food == other.food:
            return False
        if not self.capsules == other.capsules:
            return False
        if not self.score == other.score:
            return False

        return True

    def __hash__(self):
        for i, state in enumerate(self.agent_states):
            try:
                int(hash(state))
            except TypeError as e:
                print(e)

        return int((hash(tuple(self.agent_states)) + 13 *
                    hash(self.food) + 113 *
                    hash(tuple(self.capsules)) + 7 *
                    hash(self.score)) % 1048575)

    def __str__(self):
        width, height = self.layout.width, self.layout.height
        grid_map = Grid(width, height)

        if type(self.food) == type((1, 2)):
            self.food = reconstitute_grid(self.food)

        for x in range(width):
            for y in range(height):
                food, walls = self.food, self.layout.walls
                grid_map[x][y] = self._food_wall_str(food[x][y], walls[x][y])

        for agent_state in self.agent_states:
            if agent_state is None:
                continue
            if agent_state.configuration is None:
                continue

            x, y = [int(i) for i in nearest_point(agent_state.configuration.pos)]
            agent_dir = agent_state.configuration.direction

            if agent_state.is_pacman:
                grid_map[x][y] = self._pac_str(agent_dir)
            else:
                grid_map[x][y] = self._ghost_str(agent_dir)

        for x, y in self.capsules:
            grid_map[x][y] = 'o'

        return str(grid_map) + ("\nScore: %d\n" % self.score)

    @staticmethod
    def _food_wall_str(has_food, has_wall):
        if has_food:
            return '.'
        elif has_wall:
            return '%'
        else:
            return ' '

    @staticmethod
    def _pac_str(direction):
        if direction == Direction.NORTH:
            return 'v'
        if direction == Direction.SOUTH:
            return '^'
        if direction == Direction.WEST:
            return '>'
        return '<'

    @staticmethod
    def _ghost_str(_):
        return 'G'

    def initialize(self, layout, num_ghost_agents):
        self.food = layout.food.copy()
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.score_change = 0

        self.agent_states = []
        num_ghosts = 0

        for is_pacman, pos in layout.agent_positions:
            if not is_pacman:
                if num_ghosts == num_ghost_agents:
                    # Max ghosts reached already.
                    continue
                else:
                    num_ghosts += 1
            self.agent_states.append(AgentState(Configuration(pos, Direction.STOP), is_pacman))

        self._eaten = [False for _ in self.agent_states]
