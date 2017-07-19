from game.direction import Direction
from game.actions import Actions
from utilities import nearest_point, manhattan_distance


class GhostRules:
    GHOST_SPEED = 1.0

    # How close ghosts must be to pacman to kill him.
    COLLISION_TOLERANCE = 0.7

    def get_legal_actions(state, ghost_index):
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """
        conf = state.get_ghost_state(ghost_index).configuration
        possible_actions = Actions.get_possible_actions(conf, state.data.layout.walls)
        reverse = Actions.reverse_direction(conf.direction)

        if Direction.STOP in possible_actions:
            possible_actions.remove(Direction.STOP)

        if reverse in possible_actions and len(possible_actions) > 1:
            possible_actions.remove(reverse)

        return possible_actions

    get_legal_actions = staticmethod(get_legal_actions)

    def apply_action(state, action, ghost_index):
        legal = GhostRules.get_legal_actions(state, ghost_index)

        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghost_state = state.data.agent_states[ghost_index]
        speed = GhostRules.GHOST_SPEED

        if ghost_state.scared_timer > 0:
            speed /= 2.0

        vector = Actions.direction_to_vector(action, speed)
        ghost_state.configuration = ghost_state.configuration.generate_successor(vector)

    apply_action = staticmethod(apply_action)

    def decrement_timer(ghost_state):
        timer = ghost_state.scared_timer

        if timer == 1:
            ghost_state.configuration.pos = nearest_point(ghost_state.configuration.pos)

        ghost_state.scared_timer = max(0, timer - 1)

    decrement_timer = staticmethod(decrement_timer)

    def check_death(state, agent_index):
        pacman_position = state.get_pacman_position()

        if agent_index == 0:
            # Pacman just moved; anyone can kill him.
            for index in range(1, len(state.data.agent_states)):
                ghost_state = state.data.agent_states[index]
                ghost_position = ghost_state.configuration.get_position()

                if GhostRules.can_kill(pacman_position, ghost_position):
                    GhostRules.collide(state, ghost_state, index)
        else:
            ghost_state = state.data.agent_states[agent_index]
            ghost_position = ghost_state.configuration.get_position()

            if GhostRules.can_kill(pacman_position, ghost_position):
                GhostRules.collide(state, ghost_state, agent_index)

    check_death = staticmethod(check_death)

    def collide(state, ghost_state, agent_index):
        if ghost_state.scared_timer > 0:
            state.data.score_change += 200
            GhostRules.place_ghost(state, ghost_state)
            ghost_state.scared_timer = 0
            # Added for first-person.
            state.data._eaten[agent_index] = True
        else:
            if not state.data._win:
                state.data.score_change -= 500
                state.data._lose = True

    collide = staticmethod(collide)

    def can_kill(pacman_position, ghost_position):
        return manhattan_distance(ghost_position, pacman_position) <= GhostRules.COLLISION_TOLERANCE

    can_kill = staticmethod(can_kill)

    def place_ghost(state, ghost_state):
        ghost_state.configuration = ghost_state.start

    place_ghost = staticmethod(place_ghost)
