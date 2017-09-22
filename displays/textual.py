from __future__ import print_function

import pacumen
import time

DRAW_EVERY = 1
SLEEP_TIME = 0
DISPLAY_MOVES = False
QUIET = False


class NullGraphics:
    def initialize(self, state, is_blue=False):
        pass

    def update(self, state):
        pass

    def check_null_display(self):
        return True

    def pause(self):
        time.sleep(SLEEP_TIME)

    def draw(self, state):
        print(state)

    def update_distributions(self, dist):
        pass

    def finish(self):
        pass


class PacmanDisplay:
    def __init__(self, speed=None):
        if speed is not None:
            global SLEEP_TIME
            SLEEP_TIME = speed

    def initialize(self, state, is_blue=False):
        self.draw(state)
        self.pause()
        self.turn = 0
        self.agent_counter = 0

    def update(self, state):
        num_agents = len(state.agent_states)
        self.agent_counter = (self.agent_counter + 1) % num_agents

        if self.agent_counter == 0:
            self.turn += 1
            if DISPLAY_MOVES:
                ghosts = [pacumen.nearest_point(state.agent_states[i].get_position()) for i in range(1, num_agents)]
                print("%4d) P: %-8s" %
                      (self.turn, str(pacumen.nearest_point(state.agent_states[0].get_position()))),
                      '| Score: %-5d' % state.score, '| Ghosts:', ghosts)

            if self.turn % DRAW_EVERY == 0:
                self.draw(state)
                self.pause()

        if state._win or state._lose:
            self.draw(state)

    def pause(self):
        time.sleep(SLEEP_TIME)

    def draw(self, state):
        print(state)

    def finish(self):
        pass
