from agents_learning import ReinforcementAgent
from game.feature_extractors import *

import random
import logging
import utilities


class QLearningAgent(ReinforcementAgent):
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        # q-values maps (state, action) to q-value
        self.q_values = utilities.Counter()

    def get_q_value(self, state, action):
        """
        Returns Q(state, action). This should return 0.0 if the agent has
        never seen a state or the Q node value otherwise.
        """
        if (state, action) not in self.q_values:
            self.q_values[(state, action)] = 0.0

        return self.q_values[(state, action)]

    def compute_value_from_q_values(self, state):
        """
        Returns max_action Q(state, action) where the max is over the legal
        actions. Note that if there are no legal actions, which is the case
        at the terminal state, this should return a value of 0.0.
        """
        # policy = self.get_policy(state)
        # value = self.get_q_value(state, policy)
        # return value
        legal_actions = self.get_legal_actions(state)

        if len(legal_actions) == 0:
            return 0.0

        value = utilities.Counter()

        for action in legal_actions:
            value[action] = self.get_q_value(state, action)

        return value[value.arg_max()]

    def compute_action_from_q_values(self, state):
        """
        Computes the best action to take in a state. Note that if there
        are no legal actions, which is the case at the terminal state,
        this should return None.
        """
        # best_action, best_value = (None, float('-inf'))
        # actions = self.get_legal_actions(state)

        # for action in actions:
        #    q_value = self.get_q_value(state, action)
        #    if q_value > best_value:
        #        best_action, best_value = action, q_value

        # return best_action
        legal_actions = self.get_legal_actions(state)

        if len(legal_actions) == 0:
            return None

        value = utilities.Counter()

        for action in legal_actions:
            value[action] = self.get_q_value(state, action)

        actions = value.arg_max(all_max=True)

        return random.choice(actions)

    def get_action(self, state):
        """
        Computes the action to take in the current state. With probability
        self.epsilon, this should take a random action or, otherwise, take
        whatever is the best policy action. Note that if there are no legal
        actions available, which is the case at the terminal state, this
        should choose None as the action.
        """
        legal_actions = self.get_legal_actions(state)
        action = None

        if len(legal_actions) != 0:
            if utilities.flip_coin(self.epsilon):
                action = random.choice(legal_actions)
            else:
                action = self.get_policy(state)
                # action = self.compute_action_from_q_values(state)

        return action

    def update(self, state, action, next_state, reward):
        """
        This is called to observe a state = action => next_state and reward
        transition. This is where q-values are updated.
        """
        # q-value is updated via q-learning
        # new_Q(s,a) = (1 - alpha) * old_Q(s,a) + alpha * (reward + discount * future rewards)
        # new_Q(s,a) = old_Q(s,a) + alpha (reward + discount * future rewards - old_Q(s,a))
        # print("State: ", state, " , Action: ", action, " , NextState: ", next_state, " , Reward: ", reward)
        logging.debug("\nState:\n{0}\n".format(state))
        logging.info("Action: {0}".format(action))
        logging.debug("Next State\n{0}".format(next_state))
        logging.info("Reward: {0}".format(reward))
        logging.info("Q-Value: {0}".format(self.get_q_value(state, action)))
        logging.info("State Value: {0}\n".format(self.get_value(next_state)))

        # q_value = self.get_q_value(state, action)
        # next_value = self.get_value(next_state)
        # q_value += self.alpha * (reward + self.discount * next_value - q_value)
        # self.q_values[(state, action)] = q_value

        self.q_values[(state, action)] = ((1 - self.alpha) * self.get_q_value(state, action)) + self.alpha * (reward + self.discount * self.get_value(next_state))

    def get_policy(self, state):
        return self.compute_action_from_q_values(state)

    def get_value(self, state):
        return self.compute_value_from_q_values(state)


class PacmanControlAgent(QLearningAgent):
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


class PacmanExperimentAgent(PacmanControlAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        self.feat_extractor = utilities.lookup(extractor, globals())()
        PacmanControlAgent.__init__(self, **args)
        self.weights = utilities.Counter()

    def get_weights(self):
        return self.weights

    def get_q_value(self, state, action):
        """
        This returns Q(state,action) = w * featureVector
        The * is a dot product operator.
        """
        # if no action, return zero
        if action is None:
            return 0.0

        # get feature vector
        feature_vector = self.feat_extractor.get_features(state, action)

        # q-value = sum (weights * feature values) of all features
        q_value = 0.0

        for feature in feature_vector:
            # q_value += self.weights[feature] * feature_vector[feature]
            q_value += self.get_weights()[feature] * feature_vector[feature]
            # qvals += self.getWeights()[f] * feats[f]

        return q_value

    def update(self, state, action, next_state, reward):
        """
        Updates weights based on transition.
        """
        # difference = reward + discount * future rewards - q-value
        # q_value = self.get_q_value(state, action)
        # next_value = self.get_value(next_state)
        # difference = reward + self.discount * next_value - q_value

        # update feature weights
        feature_vector = self.feat_extractor.get_features(state, action)

        # for feature in feature_vector:
        #    self.weights[feature] += self.alpha * difference * feature_vector[feature]

        self.epsilon *= 0.9995

        for feature in feature_vector:
            self.weights[feature] = self.weights[feature] + self.alpha * feature_vector[feature] * ((reward + self.discount * self.get_value(next_state)) - self.get_q_value(state, action))

    def final(self, state):
        PacmanControlAgent.final(self, state)
        # print("Completed episode #%d" % self.episodes_so_far)

        if self.episodes_so_far == self.numTraining:
            # logging.info("WEIGHTS: {0}".format(self.get_weights()))
            for state in self.get_weights():
                logging.debug("State\n{0} has weight {1}".format(state[0], self.get_weights()[state]))

            pass
