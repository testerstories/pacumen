from __future__ import print_function

import pacman
import time

DRAW_EVERY = 1
SLEEP_TIME = 0
DISPLAY_MOVES = False
QUIET = False


class NullGraphics:
    def initialize(self, state, isBlue = False):
        pass

    def update(self, state):
        pass

    def checkNullDisplay(self):
        return True

    def pause(self):
        time.sleep(SLEEP_TIME)

    def draw(self, state):
        print(state)

    def updateDistributions(self, dist):
        pass

    def finish(self):
        pass


class PacmanDisplay:
    def __init__(self, speed=None):
        if speed != None:
            global SLEEP_TIME
            SLEEP_TIME = speed

    def initialize(self, state, isBlue = False):
        self.draw(state)
        self.pause()
        self.turn = 0
        self.agentCounter = 0

    def update(self, state):
        num_agents = len(state.agent_states)
        self.agentCounter = (self.agentCounter + 1) % num_agents

        if self.agentCounter == 0:
            self.turn += 1
            if DISPLAY_MOVES:
                ghosts = [pacman.nearestPoint(state.get_ghost_position(i)) for i in range(1, num_agents)]
                print("%4d) P: %-8s" % (self.turn, str(pacman.nearestPoint(state.get_pacman_position()))), '| Score: %-5d' % state.score, '| Ghosts:', ghosts)

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
