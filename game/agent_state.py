class AgentState:
    def __init__(self, start_configuration, is_pacman):
        self.start = start_configuration
        self.configuration = start_configuration
        self.is_pacman = is_pacman
        self.scared_timer = 0
        self.num_carrying = 0
        self.num_returned = 0

    def __str__(self):
        if self.is_pacman:
            return "Pacman: " + str(self.configuration)
        else:
            return "Ghost: " + str(self.configuration)

    def __eq__(self, other):
        if other is None:
            return False

        return self.configuration == other.configuration and self.scared_timer == other.scared_timer

    def __hash__(self):
        return hash(hash(self.configuration) + 13 * hash(self.scared_timer))

    def copy(self):
        state = AgentState(self.start, self.is_pacman)
        state.configuration = self.configuration
        state.scared_timer = self.scared_timer
        state.num_carrying = self.num_carrying
        state.num_returned = self.num_returned
        return state

    def get_position(self):
        if self.configuration is None:
            return None

        return self.configuration.get_position()

    def get_direction(self):
        return self.configuration.get_direction()
