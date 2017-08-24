from utilities import manhattan_distance
from game.direction import Direction
from game.agent import Agent

import random
import utilities


class ScoreReflexAgent(Agent):
    def get_action(self, game_state):
        legal_moves = game_state.get_legal_actions()

        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices)

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghost_state.scared_timer for ghost_state in new_ghost_states]

        return successor_game_state.get_score()


class UtilityReflexAgent(Agent):
    def get_action(self, game_state):
        legal_moves = game_state.get_legal_actions()

        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices)

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghost_state.scared_timer for ghost_state in new_ghost_states]

        # Utility of ghosts.
        # Decrease utility of ghosts when they are three steps or closer.
        u_ghosts = 0
        min_distance_away = 3

        for ghost_state in new_ghost_states:
            u_ghost = manhattan_distance(new_pos, ghost_state.get_position())
            u_ghost = (min(min_distance_away, u_ghost) - min_distance_away) * 999
            u_ghosts += u_ghost

        # Utility of food.
        # Discounted rewards for being further away from food.
        u_food = 0
        food_list = new_food.as_list()

        for food in food_list:
            u_food += 1 / float(manhattan_distance(new_pos, food))

        score = successor_game_state.get_score()
        utility = score + u_food + u_ghosts

        return utility


class EvaluateReflexAgent(Agent):
    def get_action(self, game_state):
        legal_moves = game_state.get_legal_actions()

        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices)

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        successor_game_state = current_game_state.generate_pacman_successor(action)
        new_pos = successor_game_state.get_pacman_position()
        new_food = successor_game_state.get_food()
        new_ghost_states = successor_game_state.get_ghost_states()
        new_scared_times = [ghost_state.scared_timer for ghost_state in new_ghost_states]

        successor_game_state = current_game_state.generate_pacman_successor(action)

        return better_evaluation_function(successor_game_state)


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
    # Evaluation of a game state will be based on various utilities.
    score = current_game_state.get_score()
    position = current_game_state.get_pacman_position()

    # Constants to be used in balancing utilities -- a lot of guesswork and
    # magic numbers.
    food_constant = 1
    capsule_constant = 20
    ghost_constant = 100

    # Food
    # The utility of food will be reduced the further away it is from pacman
    u_food = 0
    food_grid = current_game_state.get_food()
    food_list = food_grid.as_list()

    for food in food_list:
        u_food += food_constant / float(manhattan_distance(position, food))

    # Capsules
    # The utility of capsules will be reduced the further away it is from
    # pacman.
    u_capsules = 0
    capsules = current_game_state.get_capsules()

    for capsule in capsules:
        u_capsules += capsule_constant / float(manhattan_distance(position, capsule))

    # Scared Ghosts
    # When ghosts are scared (edible), the utility of ghosts will be reduced
    # the further away it is from pacman.
    u_ghosts = 0
    ghost_states = current_game_state.get_ghost_states()

    for ghost_index, ghost_state in enumerate(ghost_states):
        if ghost_state.scared_timer:
            ghost_position = ghost_states[ghost_index].get_position()
            u_ghosts += ghost_constant / float(manhattan_distance(position, ghost_position))

    # Sum estimated utilities.
    utility = score + u_food + u_capsules + u_ghosts

    return utility


# Abbreviation
better = better_evaluation_function
