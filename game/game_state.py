from game_state_data import GameStateData

from rules.pacman_rules import PacmanRules
from rules.ghost_rules import GhostRules


class GameState:
    """
    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes.

    GameStates are used by the Game object to capture the actual state of the
    game and can be used by agents to reason about the game.

    Much of the information in a GameState is stored in a GameStateData
    object. We strongly suggest that you access that data via the accessor
    methods below rather than referring to the GameStateData object directly.

    Note that in classic Pacman, Pacman is always agent 0.
    """

    # Number of points lost each round.
    TIME_PENALTY = 1

    ####################################################
    # Accessor methods: use these to access state data #
    ####################################################

    # static variable keeps track of which states have had getLegalActions called
    explored = set()

    def get_and_reset_explored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp

    get_and_reset_explored = staticmethod(get_and_reset_explored)

    def get_legal_actions(self, agent_index=0):
        """
        Returns the legal actions for the agent specified.
        """
        # GameState.explored.add(self)
        if self.is_win() or self.is_lose():
            return []

        if agent_index == 0:
            # Pacman is moving.
            return PacmanRules.get_legal_actions(self)
        else:
            return GhostRules.get_legal_actions(self, agent_index)

    def generate_successor(self, agent_index, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        # Check that successors exist.
        if self.is_win() or self.is_lose():
            raise Exception("Unable to generate a successor of a terminal state.")

        # Copy current state.
        state = GameState(self)

        # Let agent's logic deal with its action's effects on the board.
        if agent_index == 0:
            # Pacman is moving.
            state.data._eaten = [False for i in range(state.get_num_agents())]
            PacmanRules.apply_action(state, action)
        else:
            # A ghost is moving.
            GhostRules.apply_action(state, action, agent_index)

        # Time passes.
        if agent_index == 0:
            state.data.score_change += -GameState.TIME_PENALTY
        else:
            GhostRules.decrement_timer(state.data.agent_states[agent_index])

        # Resolve multi-agent effects.
        GhostRules.check_death(state, agent_index)

        # Book keeping.
        state.data._agent_moved = agent_index
        state.data.score += state.data.score_change
        GameState.explored.add(self)
        GameState.explored.add(state)

        return state

    def get_legal_pacman_actions(self):
        return self.get_legal_actions(0)

    def generate_pacman_successor(self, action):
        """
        Generates the successor state after the specified pacman move
        """
        return self.generate_successor(0, action)

    def get_pacman_state(self):
        """
        Returns an AgentState object for pacman (in game.py)

        state.pos gives the current position
        state.direction gives the travel vector
        """
        return self.data.agent_states[0].copy()

    def get_pacman_position(self):
        return self.data.agent_states[0].get_position()

    def get_ghost_states(self):
        return self.data.agent_states[1:]

    def get_ghost_state(self, agent_index):
        if agent_index == 0 or agent_index >= self.get_num_agents():
            raise Exception("Invalid index passed to getGhostState")

        return self.data.agent_states[agent_index]

    def get_ghost_position(self, agent_index):
        if agent_index == 0:
            raise Exception("Pac-Man's index passed to getGhostPosition")

        return self.data.agent_states[agent_index].get_position()

    def get_ghost_positions(self):
        return [s.get_position() for s in self.get_ghost_states()]

    def get_num_agents(self):
        return len(self.data.agent_states)

    def get_score(self):
        return float(self.data.score)

    def get_capsules(self):
        """
        Returns a list of positions (x,y) of the remaining capsules.
        """
        return self.data.capsules

    def get_num_food(self):
        return self.data.food.count()

    def get_food(self):
        """
        Returns a Grid of boolean food indicator variables.

        Grids can be accessed via list notation, so to check
        if there is food at (x,y), just call

        currentFood = state.getFood()
        if currentFood[x][y] == True: ...
        """
        return self.data.food

    def get_walls(self):
        """
        Returns a Grid of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.data.layout.walls

    def has_food(self, x, y):
        return self.data.food[x][y]

    def has_wall(self, x, y):
        return self.data.layout.walls[x][y]

    def is_lose(self):
        return self.data._lose

    def is_win(self):
        return self.data._win

    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################

    def __init__(self, previous_state=None):
        """
        Generates a new state by copying information from its predecessor.
        """
        if previous_state is not None:
            self.data = GameStateData(previous_state.data)
        else:
            self.data = GameStateData()

    def deep_copy(self):
        state = GameState(self)
        state.data = self.data.deep_copy()
        return state

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        return hasattr(other, 'data') and self.data == other.data

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.data)

    def __str__(self):

        return str(self.data)

    def initialize(self, layout, num_ghost_agents=1000):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        self.data.initialize(layout, num_ghost_agents)
