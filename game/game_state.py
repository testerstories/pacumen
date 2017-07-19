from .game_state_data import GameStateData

from rules.pacman_rules import PacmanRules
from rules.ghost_rules import GhostRules


class GameState:
    # Number of points lost each round.
    TIME_PENALTY = 1

    # Static variable keeps track of which states have had
    # get_legal_actions called.
    explored = set()

    def get_and_reset_explored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp

    get_and_reset_explored = staticmethod(get_and_reset_explored)

    def get_legal_actions(self, agent_index=0):
        # GameState.explored.add(self)
        if self.is_win() or self.is_lose():
            return []

        if agent_index == 0:
            return PacmanRules.get_legal_actions(self)
        else:
            return GhostRules.get_legal_actions(self, agent_index)

    def generate_successor(self, agent_index, action):
        # Check that successors exist.
        if self.is_win() or self.is_lose():
            raise Exception("Unable to generate a successor of a terminal state.")

        # Copy current state.
        state = GameState(self)

        # Let agent logic deal with its actions effect on the board.
        if agent_index == 0:
            state.data._eaten = [False for _ in range(state.get_num_agents())]
            PacmanRules.apply_action(state, action)
        else:
            GhostRules.apply_action(state, action, agent_index)

        # Time passes.
        if agent_index == 0:
            state.data.score_change += -GameState.TIME_PENALTY
        else:
            GhostRules.decrement_timer(state.data.agent_states[agent_index])

        # Resolve multi-agent effects.
        GhostRules.check_death(state, agent_index)

        # General state bookkeeping.
        state.data._agent_moved = agent_index
        state.data.score += state.data.score_change
        GameState.explored.add(self)
        GameState.explored.add(state)

        return state

    def get_legal_pacman_actions(self):
        return self.get_legal_actions(0)

    def generate_pacman_successor(self, action):
        return self.generate_successor(0, action)

    def get_pacman_state(self):
        return self.data.agent_states[0].copy()

    def get_pacman_position(self):
        return self.data.agent_states[0].get_position()

    def get_ghost_states(self):
        return self.data.agent_states[1:]

    def get_ghost_state(self, agent_index):
        if agent_index == 0 or agent_index >= self.get_num_agents():
            raise Exception("Invalid index passed to get_ghost_state")

        return self.data.agent_states[agent_index]

    def get_ghost_position(self, agent_index):
        if agent_index == 0:
            raise Exception("Pac-Man's index passed to get_ghost_position")

        return self.data.agent_states[agent_index].get_position()

    def get_ghost_positions(self):
        return [s.get_position() for s in self.get_ghost_states()]

    def get_num_agents(self):
        return len(self.data.agent_states)

    def get_score(self):
        return float(self.data.score)

    def get_capsules(self):
        return self.data.capsules

    def get_num_food(self):
        return self.data.food.count()

    def get_food(self):
        return self.data.food

    def get_walls(self):
        return self.data.layout.walls

    def has_food(self, x, y):
        return self.data.food[x][y]

    def has_wall(self, x, y):
        return self.data.layout.walls[x][y]

    def is_lose(self):
        return self.data._lose

    def is_win(self):
        return self.data._win

    def __init__(self, previous_state=None):
        if previous_state is not None:
            self.data = GameStateData(previous_state.data)
        else:
            self.data = GameStateData()

    def deep_copy(self):
        state = GameState(self)
        state.data = self.data.deep_copy()
        return state

    def __eq__(self, other):
        return hasattr(other, 'data') and self.data == other.data

    def __hash__(self):
        return hash(self.data)

    def __str__(self):
        return str(self.data)

    def initialize(self, layout, num_ghost_agents=1000):
        self.data.initialize(layout, num_ghost_agents)
