from agents_learning import ReinforcementAgent
from game.feature_extractors import *

import utilities


class QLearningAgent(ReinforcementAgent):
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"

    def get_q_value(self, state, action):
        utilities.raise_not_defined()

    def compute_value_from_q_values(self, state):
        utilities.raise_not_defined()

    def compute_action_from_q_values(self, state):
        utilities.raise_not_defined()

    def get_action(self, state):
        legal_actions = self.get_legal_actions(state)
        action = None

        utilities.raise_not_defined()

        return action

    def update(self, state, action, next_state, reward):
        utilities.raise_not_defined()

    def get_policy(self, state):
        return self.compute_action_from_q_values(state)

    def get_value(self, state):
        return self.compute_value_from_q_values(state)


class PacmanQAgent(QLearningAgent):
    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0
        QLearningAgent.__init__(self, **args)

    def get_action(self, state):
        action = QLearningAgent.get_action(self, state)
        self.do_action(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        self.feat_extractor = utilities.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = utilities.Counter()

    def get_weights(self):
        return self.weights

    def get_q_value(self, state, action):
        utilities.raise_not_defined()

    def update(self, state, action, next_state, reward):
        utilities.raise_not_defined()

    def final(self, state):
        PacmanQAgent.final(self, state)

        if self.episodes_so_far == self.numTraining:
            "*** YOUR CODE HERE ***"
            pass
