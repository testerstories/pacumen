import utilities


class MarkovDecisionProcess:
    """
    This class provides methods that are relevant for a general markov
    decision process.
    """

    def get_states(self):
        """
        Returns a list of all states in the MDP. Note that this is not
        generally possible for large MDPs.
        """
        utilities.abstract()

    def get_start_state(self):
        """
        Returns the start state of the MDP.
        """
        utilities.abstract()

    def get_possible_actions(self, state):
        """
        Returns a list of possible actions from the current state.
        """
        utilities.abstract()

    def get_transition_states_and_probs(self, state, action):
        """
        Returns a list of (next_state, prob) pairs representing the states
        reachable from 'state' by taking 'action' along with their transition
        probabilities.

        Note that in Q-Learning and reinforcement learning in general, we
        won't know these probabilities nor do we directly model them.
        """
        utilities.abstract()

    def get_reward(self, state, action, next_state):
        """
        Gets the reward for the state, action, next_state transition.

        Note that this is not available in reinforcement learning.
        """
        utilities.abstract()

    def is_terminal(self, state):
        """
        Returns true if the current state is a terminal state.

        Note that, by convention, a terminal state has zero future rewards.
        It's possible that the terminal state(s) have no possible actions.
        It's  also common to think of the terminal state as having a type of
        self-loop action 'pass' with zero reward. Those formulations are
        essentially equivalent.
        """
        utilities.abstract()
