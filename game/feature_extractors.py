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
    """
    Find the closest reachable food pellet.
    """
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
    return 0.0  # WAS NONE


def smallest_food_path(pos, food, walls):
    """
    Determine how many food pellets are left on the current path (up to 5).
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()

    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        expanded.add((pos_x, pos_y))

        # Spread out from the current location to its neighbors.
        neighbors = Actions.get_legal_neighbors((pos_x, pos_y), walls)

        count_with_food = 0

        for nbr_x, nbr_y in neighbors:
            if (nbr_x, nbr_y) not in expanded and food[nbr_x][nbr_y]:
                fringe.append((nbr_x, nbr_y, dist+1))
                count_with_food += 1

        if count_with_food == 0 and food[pos_x][pos_y] or dist == 5: # dist > 0 ?
            return dist

    # No food was found.
    return 5


def closest_capsule(pos, capsules, walls):
    """
    Find the closest capsule (max distance 5).
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()

    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)

        if (pos_x, pos_y) in expanded:
            continue

        expanded.add((pos_x, pos_y))

        # If the agent finds a capsule at this location, then exit.
        if (pos_x, pos_y) in capsules or dist == 5:
            return dist

        # Otherwise spread out from this location to its neighbors.
        neighbors = Actions.get_legal_neighbors((pos_x, pos_y), walls)

        for nbr_x, nbr_y in neighbors:
            fringe.append((nbr_x, nbr_y, dist+1))

    # No capsule was found.
    return 0.0


def closest_ghost(pos, ghosts, walls):
    """
    Find the minimum distance to ghosts.
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()

    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)

        if (pos_x, pos_y) in expanded:
            continue

        expanded.add((pos_x, pos_y))

        # If the agent finds a ghost at this location, then exit.
        for ghost in ghosts:
            g_x, g_y = ghost.get_position()

            if (int(g_x), int(g_y)) == (pos_x, pos_y):
                return ghost, dist

        # Otherwise spread out from this location to its neighbors.
        neighbors = Actions.get_legal_neighbors((pos_x, pos_y), walls)

        for nbr_x, nbr_y in neighbors:
            fringe.append((nbr_x, nbr_y, dist+1))

    # No ghost was found.
    return None, dist


class TacticExtractor(FeatureExtractor):
    """
    Returns features for a pacman agent that is largely being tactical
    in terms of how it learns the game.

    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """
    def get_features(self, state, action):
        # Extract the grid of food, wall locations, and the ghost
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


class StrategyExtractor(FeatureExtractor):
    """
    Returns features for a pacman agent that considers more aspects of
    the game in terms of a strategy to win with the highest possible
    score.
    """
    def get_features(self, state, action):
        # Extract the grid of food, power pellets, wall locations, and
        # ghost states.
        food = state.get_food()
        capsules = state.get_capsules()
        walls = state.get_walls()
        ghosts = state.get_ghost_states()
        scared_ghosts = [ghost for ghost in ghosts if ghost.scared_timer > 0]
        not_scared_ghosts = [ghost for ghost in ghosts if ghost.scared_timer == 0]

        features = utilities.Counter()

        # features["bias"] = 0.5

        # Compute the location of pacman after he takes the action.
        x, y = state.get_pacman_position()
        dx, dy = Actions.direction_to_vector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # Count the number of ghosts that are one step away.
        features["#-of-ghosts-1-step-away"] = 0.0

        if not_scared_ghosts and closest_ghost((next_x, next_y), not_scared_ghosts, walls)[1] <= 2:
            features["#-of-ghosts-1-step-away"] = 1.0

        # Eat a scared ghost (continue in "closest scared ghost")
        features["eats-scared-ghost"] = 0.0

        # Ghost spawn location (continue in "closest scared ghost")
        # features["at-ghost-spawn-location"] = 0.0
        # start position state.data.agent_states[index].start.get_position()

        # Look for the closest scared ghost.
        features["closest-scared-ghost"] = 0.0

        if scared_ghosts and not features["#-of-ghosts-1-step-away"]:
            closest, dist = closest_ghost((next_x, next_y), scared_ghosts, walls)

            if not features["#-of-ghosts-1-step-away"] and dist <= 1.0:
                features["eats-scared-ghost"] = 0.5

            if (closest.scared_timer / 2.0 > dist) and closest.scared_timer >= 2:
                features["closest-scared-ghost"] = (closest.scared_timer / 2.0 - dist) / 50.0

            # if closest.start.get_position() == (next_x, next_y) and features["eats-scared-ghost"]:
            #     features["at-ghost-spawn-location"] = 1.0

        should_chase = features["closest-scared-ghost"] > 0.0

        # If there is no danger of ghosts then add the food feature.
        features["eats-food"] = 0.0

        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 0.1

        # Eat small path (< 5) of food before if there is a choice.
        features["eat-small-path-food"] = 0.0

        if features["eats-food"]:
            features["eat-small-path-food"] = (5.0 - smallest_food_path((next_x, next_y), food, walls)) / 50.0

        dist = closest_food((next_x, next_y), food, walls)
        features["closest-food"] = 0.0

        if dist is not None:
            # Make the distance a number less than 1 otherwise the update
            # will diverge wildly.
            features["closest-food"] = float(dist) / (walls.width * walls.height)

        # Consider capsules.
        features["capsule-nearby"] = 0.0

        if not features["#-of-ghosts-1-step-away"] and capsules:
            features["capsule-nearby"] = (5 - closest_capsule((next_x, next_y), capsules, walls)) / 10.0

        # Stopped
        # features["stopped"] = 1.0 if action == 'Stop' else 0.0

        # Decrement all other features if pacman is chasing a ghost.
        if should_chase:
            features["eats-food"] /= 10.0
            features["closest-food"] /= 10.0
            features["capsule-nearby"] /= 10.0
            features["eat-small-path-food"] /= 10.0

        features.divide_all(10.0)

        return features
