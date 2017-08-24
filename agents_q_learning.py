from agents_learning import ReinforcementAgent
from game.feature_extractors import *

import random
import utilities


class QLearningAgent(ReinforcementAgent):
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        # q-values maps (state, action) to q-value
        self.qvalues = utilities.Counter()

    def get_q_value(self, state, action):
        return self.qvalues[(state, action)]

    def compute_value_from_q_values(self, state):
        policy = self.get_policy(state)
        value = self.get_q_value(state, policy)
        return value

    def compute_action_from_q_values(self, state):
        best_action, best_value = (None, float('-inf'))
        actions = self.get_legal_actions(state)

        for action in actions:
            qvalue = self.get_q_value(state, action)
            if qvalue > best_value:
                best_action, best_value = action, qvalue

        return best_action

    def get_action(self, state):
        legal_actions = self.get_legal_actions(state)
        action = None

        if utilities.flip_coin(self.epsilon):
            action = random.choice(legal_actions)
        else:
            action = self.get_policy(state)

        return action

    def update(self, state, action, next_state, reward):
        # q-value is updated via q-learning
        # new_Q(s,a) = (1 - alpha) * old_Q(s,a) + alpha * (reward + discount * future rewards)
        # new_Q(s,a) = old_Q(s,a) + alpha (reward + discount * future rewards - old_Q(s,a))
        q_value = self.get_q_value(state, action)
        next_value = self.get_value(next_state)
        q_value += self.alpha * (reward + self.discount * next_value - q_value)
        self.qvalues[(state, action)] = q_value

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
        # if no action, return zero
        if action is None:
            return 0.0

        # get feature vector
        feature_vector = self.feat_extractor.get_features(state, action)

        # q-value = sum (weights * feature values) of all features
        q_value = 0.0

        for feature in feature_vector:
            q_value += self.weights[feature] * feature_vector[feature]

        return q_value

    def update(self, state, action, next_state, reward):
        # difference = reward + discount * future rewards - q-value
        q_value = self.get_q_value(state, action)
        next_value = self.get_value(next_state)
        difference = reward + self.discount * next_value - q_value

        # update feature weights
        feature_vector = self.feat_extractor.get_features(state, action)

        for feature in feature_vector:
            self.weights[feature] += self.alpha * difference * feature_vector[feature]

    def final(self, state):
        PacmanQAgent.final(self, state)

        if self.episodes_so_far == self.numTraining:
            "*** ANY CODE NEEDED HERE? ***"
            pass
