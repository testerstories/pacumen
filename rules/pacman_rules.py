from game.actions import Actions
from utilities import nearest_point, manhattan_distance


class PacmanRules:
    PACMAN_SPEED = 1

    # Moves ghosts are scared.
    SCARED_TIME = 40

    def get_legal_actions(state):
        """
        Returns a list of possible actions.
        """
        return Actions.get_possible_actions(state.get_pacman_state().configuration, state.data.layout.walls)

    get_legal_actions = staticmethod(get_legal_actions)

    def apply_action(state, action):
        """
        Edits the state to reflect the results of the action.
        """
        legal = PacmanRules.get_legal_actions(state)

        if action not in legal:
            raise Exception("Illegal action " + str(action))

        pacman_state = state.data.agent_states[0]

        # Update Configuration
        vector = Actions.direction_to_vector(action, PacmanRules.PACMAN_SPEED)
        pacman_state.configuration = pacman_state.configuration.generate_successor(vector)

        # Eat dots.
        next = pacman_state.configuration.get_position()
        nearest = nearest_point(next)

        if manhattan_distance(nearest, next) <= 0.5:
            # Remove food when eaten.
            PacmanRules.consume(nearest, state)

    apply_action = staticmethod(apply_action)

    def consume(position, state):
        x, y = position

        # Eat food.
        if state.data.food[x][y]:
            state.data.score_change += 10
            state.data.food = state.data.food.copy()
            state.data.food[x][y] = False
            state.data._food_eaten = position

            # TODO: cache numFood?
            num_food = state.get_num_food()

            if num_food == 0 and not state.data._lose:
                state.data.score_change += 500
                state.data._win = True

        # Eat capsule.
        if position in state.get_capsules():
            state.data.capsules.remove(position)
            state.data._capsule_eaten = position
            # Reset all ghosts' scared timers.
            for index in range(1, len(state.data.agent_states)):
                state.data.agent_states[index].scared_timer = PacmanRules.SCARED_TIME

    consume = staticmethod(consume)
