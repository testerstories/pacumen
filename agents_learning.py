from game.agent import Agent
from game.direction import Direction
from game.actions import Actions

import time
import utilities


class ValueEstimationAgent(Agent):
    def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining=10):
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.numTraining = int(numTraining)

    def get_q_value(self, state, action):
        utilities.raise_not_defined()

    def get_value(self, state):
        utilities.raise_not_defined()

    def get_policy(self, state):
        utilities.raise_not_defined()

    def get_action(self, state):
        utilities.raise_not_defined()


class ReinforcementAgent(ValueEstimationAgent):
    def __init__(self, actionFn=None, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        if actionFn is None:
            actionFn = lambda state: state.get_legal_actions()

        self.actionFn = actionFn
        self.episodes_so_far = 0
        self.accum_train_rewards = 0.0
        self.accum_test_rewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

    def update(self, state, action, next_state, reward):
        utilities.raise_not_defined()

    def get_legal_actions(self, state):
        return self.actionFn(state)

    def observe_transition(self, state, action, next_state, delta_reward):
        self.episode_rewards += delta_reward
        self.update(state, action, next_state, delta_reward)

    def start_episode(self):
        self.last_state = None
        self.last_action = None
        self.episode_rewards = 0.0

    def stop_episode(self):
        if self.episodes_so_far < self.numTraining:
            self.accum_train_rewards += self.episode_rewards
        else:
            self.accum_test_rewards += self.episode_rewards

        self.episodes_so_far += 1

        if self.episodes_so_far >= self.numTraining:
            # No exploration, no learning.
            self.epsilon = 0.0
            self.alpha = 0.0

    def is_in_training(self):
        return self.episodes_so_far < self.numTraining

    def is_in_testing(self):
        return not self.is_in_training()

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def set_learning_rate(self, alpha):
        self.alpha = alpha

    def set_discount(self, discount):
        self.discount = discount

    def do_action(self, state, action):
        self.last_state = state
        self.last_action = action

    def observation_function(self, state):
        if self.last_state is not None:
            reward = state.get_score() - self.last_state.get_score()
            self.observe_transition(self.last_state, self.last_action, state, reward)

        return state

    def register_initial_state(self, state):
        self.start_episode()
        if self.episodes_so_far == 0:
            print('Beginning %d episodes of Training' % self.numTraining)

    def final(self, state):
        delta_reward = state.get_score() - self.last_state.get_score()
        self.observe_transition(self.last_state, self.last_action, state, delta_reward)
        self.stop_episode()

        if not 'episode_start_time' in self.__dict__:
            self.episode_start_time = time.time()

        if not 'last_window_accum_rewards' in self.__dict__:
            self.last_window_accum_rewards = 0.0

        self.last_window_accum_rewards += state.get_score()

        NUM_EPS_UPDATE = 100

        if self.episodes_so_far % NUM_EPS_UPDATE == 0:
            print('Reinforcement Learning Status:')
            window_avg = self.last_window_accum_rewards / float(NUM_EPS_UPDATE)

            if self.episodes_so_far <= self.numTraining:
                train_avg = self.accum_train_rewards / float(self.episodes_so_far)
                print('\tCompleted %d out of %d training episodes' % (self.episodes_so_far, self.numTraining))
                print('\tAverage Rewards over all training: %.2f' % train_avg)
            else:
                test_avg = float(self.accum_test_rewards) / (self.episodes_so_far - self.numTraining)
                print('\tCompleted %d test episodes' % (self.episodes_so_far - self.numTraining))
                print('\tAverage Rewards over testing: %.2f' % test_avg)

            print('\tAverage Rewards for last %d episodes: %.2f' % (NUM_EPS_UPDATE, window_avg))
            print('\tEpisode took %.2f seconds' % (time.time() - self.episode_start_time))

            self.last_window_accum_rewards = 0.0
            self.episode_start_time = time.time()

        if self.episodes_so_far == self.numTraining:
            msg = 'Training Done (turning off epsilon and alpha)'
            print('%s\n%s' % (msg, '-' * len(msg)))
