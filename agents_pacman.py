import random

import utilities
from game.agent import Agent
from game.direction import Direction


class LeftTurnAgent(Agent):
    """
    An agent that turns left at every opportunity.
    """
    def get_action(self, state):
        legal = state.get_legal_pacman_actions()
        current = state.get_pacman_state().configuration.direction

        if current == Direction.STOP:
            current = Direction.NORTH

        left = Direction.LEFT[current]

        if left in legal:
            return left

        if current in legal:
            return current

        if Direction.RIGHT[current] in legal:
            return Direction.RIGHT[current]

        if Direction.LEFT[left] in legal:
            return Direction.LEFT[left]

        return Direction.STOP


class GreedyAgent(Agent):
    def __init__(self, eval_function="score_evaluation"):
        self.evaluation_function = utilities.lookup(eval_function, globals())
        assert self.evaluation_function is not None

    def get_action(self, state):
        legal = state.get_legal_pacman_actions()

        if Direction.STOP in legal:
            legal.remove(Direction.STOP)

        successors = [(state.generate_successor(0, action), action) for action in legal]
        scored = [(self.evaluation_function(state), action) for state, action in successors]

        best_score = max(scored)[0]
        best_actions = [pair[1] for pair in scored if pair[0] == best_score]

        return random.choice(best_actions)


def score_evaluation(state):
    return state.get_score()
