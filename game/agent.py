from utilities import raise_not_defined


class Agent:
    """
    An agent must define a get_action method, but may also define the
    following methods which will be called if they exist:

    # inspects the starting state
    def register_initial_state(self, state)
    """
    def __init__(self, index=0):
        self.index = index

    def get_action(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture,
        sonar}.py) and must return an action from Directions.{North, South,
        East, West, Stop}
        """
        raise_not_defined()
