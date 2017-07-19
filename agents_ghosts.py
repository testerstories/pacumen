import utilities
from game.actions import Actions
from game.agent import Agent
from game.direction import Direction
from utilities import manhattan_distance


class GhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    def get_action(self, state):
        dist = self.get_distribution(state)
        if len(dist) == 0:
            return Direction.STOP
        else:
            return utilities.choose_from_distribution(dist)

    def get_distribution(self, state):
        """
        Returns a Counter encoding a distribution over actions from the
        provided state.
        """
        utilities.raise_not_defined()


class RandomGhost(GhostAgent):
    """
    A ghost that chooses a legal action uniformly at random.
    """
    def get_distribution(self, state):
        dist = utilities.Counter()

        for a in state.get_legal_actions(self.index):
            dist[a] = 1.0

        dist.normalize()
        return dist


class DirectionalGhost(GhostAgent):
    """
    A ghost that prefers to rush Pac-Man, or flee when scared.
    """
    def __init__(self, index, prob_attack=0.8, prob_scared_flee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scared_flee

    def get_distribution(self, state):
        ghost_state = state.get_ghost_state(self.index)
        legal_actions = state.get_legal_actions(self.index)
        pos = state.get_ghost_position(self.index)
        is_scared = ghost_state.scared_timer > 0

        speed = 1
        if is_scared:
            speed = 0.5

        action_vectors = [Actions.direction_to_vector(a, speed) for a in legal_actions]
        new_positions = [(pos[0] + a[0], pos[1] + a[1]) for a in action_vectors]
        pacman_position = state.get_pacman_position()

        # Select best actions given the state.
        distances_to_pacman = [manhattan_distance(pos, pacman_position) for pos in new_positions]

        if is_scared:
            best_score = max(distances_to_pacman)
            best_prob = self.prob_scaredFlee
        else:
            best_score = min(distances_to_pacman)
            best_prob = self.prob_attack

        best_actions = [action for action, distance in zip(legal_actions, distances_to_pacman) if distance == best_score]

        # Construct distribution.
        dist = utilities.Counter()

        for a in best_actions:
            dist[a] = best_prob / len(best_actions)

        for a in legal_actions:
            dist[a] += (1 - best_prob) / len(legal_actions)

        dist.normalize()
        return dist
