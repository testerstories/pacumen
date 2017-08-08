import utilities
import game.mdp

from agents_learning import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    def __init__(self, mdp, discount=0.9, iterations=100):
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = utilities.Counter()

        # Write value iteration code here.

        "*** YOUR CODE HERE ***"

    def get_value(self, state):
        return self.values[state]

    def compute_q_value_from_values(self, state, action):
        utilities.raise_not_defined()

    def compute_action_from_values(self, state):
        utilities.raise_not_defined()

    def get_policy(self, state):
        return self.compute_action_from_values(state)

    def get_action(self, state):
        return self.compute_action_from_values(state)

    def get_q_value(self, state, action):
        return self.compute_q_value_from_values(state, action)
