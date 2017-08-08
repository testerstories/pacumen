import utilities

from .direction import Direction
from .actions import Actions


class FeatureExtractor:
    def get_features(self, state, action):
        """
        Returns a dictionary from features to counts. Usually, the count
        will just be 1.0 for indicator functions.
        """
        utilities.raise_not_defined()


class IdentityExtractor(FeatureExtractor):
    def get_features(self, state, action):
        feats = utilities.Counter()
        feats[(state, action)] = 1.0
        return feats


class CoordinateExtractor(FeatureExtractor):
    def get_features(self, state, action):
        feats = utilities.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats


def closest_food(pos, food, walls):
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()

    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)

        if (pos_x, pos_y) in expanded:
            continue

        expanded.add((pos_x, pos_y))

        # If the agent finds a food dot at this location, then exit.
        if food[pos_x][pos_y]:
            return dist

        # Otherwise spread out from this location to its neighbors.
        neighbors = Actions.get_legal_neighbors((pos_x, pos_y), walls)

        for nbr_x, nbr_y in neighbors:
            fringe.append((nbr_x, nbr_y, dist+1))

    # No food was found.
    return None


class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:

    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """
    def get_features(self, state, action):
        # Extract the grid of food and wall locations and get the ghost
        # locations.
        food = state.get_food()
        walls = state.get_walls()
        ghosts = state.get_ghost_positions()

        features = utilities.Counter()

        features["bias"] = 1.0

        # Compute the location of pacman after he takes the action.
        x, y = state.get_pacman_position()
        dx, dy = Actions.direction_to_vector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # Count the number of ghosts that are one step away.
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.get_legal_neighbors(g, walls) for g in ghosts)

        # If there is no danger of ghosts then add the food feature.
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closest_food((next_x, next_y), food, walls)

        if dist is not None:
            # Make the distance a number less than one otherwise the update
            # will diverge wildly.
            features["closest-food"] = float(dist) / (walls.width * walls.height)

        features.divide_all(10.0)

        return features
