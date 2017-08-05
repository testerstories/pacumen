from utilities import manhattan_distance
from game.direction import Direction
from game.agent import Agent

import random
import utilities


class ReflexAgent(Agent):
    def get_action(self, game_state):
        legal_moves = game_state.get_legal_actions()

        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices)

        "*** YOUR CODE HERE (IF WANTED) ***"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghost_state.scared_timer for ghost_state in new_ghost_states]

        "*** YOUR CODE HERE ***"

        return successor_game_state.get_score()


class MultiAgentSearchAgent(Agent):
    def __init__(self, eval_fn='score_evaluation_function', depth='2'):
        self.index = 0
        self.evaluation_function = utilities.lookup(eval_fn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        utilities.raise_not_defined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        utilities.raise_not_defined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        utilities.raise_not_defined()


def score_evaluation_function(current_game_state):
    return current_game_state.get_score()


def better_evaluation_function(current_game_state):
    utilities.raise_not_defined()


# Abbreviation
better = better_evaluation_function
