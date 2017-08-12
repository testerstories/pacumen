import utilities


class Environment:
    """
    This class is used to provide a reinforcement learning abstract class
    for markov decision process formulations and reinforcement learning.
    """

    def get_current_state(self):
        """
        Returns the current state of enviornment
        """
        utilities.abstract()

    def get_possible_actions(self, state):
        """
        Returns possible actions the agent can take in the given state.
        Can return the empty list if we are in a terminal state.
        """
        utilities.abstract()

    def do_action(self, action):
        """
        Performs the given action in the current environment state and
        updates the environment. Returns a (reward, next_state) pair.
        """
        utilities.abstract()

    def reset(self):
        """
        Resets the current state to the start state.
        """
        utilities.abstract()

    def is_terminal(self):
        """
        Checks if the environment has entered a terminal state. This means
        there are no successors.
        """
        state = self.get_current_state()
        actions = self.get_possible_actions(state)
        return len(actions) == 0
