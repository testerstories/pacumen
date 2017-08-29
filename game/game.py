from utilities import *
import time
import traceback
import sys
import logging


try:
    import boinc
    _BOINC_ENABLED = True
except ImportError:
    _BOINC_ENABLED = False


class Game:
    def __init__(self, agents, display, rules, starting_index=0, mute_agents=False, catch_exceptions=False):
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.starting_index = starting_index
        self.game_over = False
        self.mute_agents = mute_agents
        self.catch_exceptions = catch_exceptions
        self.move_history = []
        self.total_agent_times = [0 for _ in agents]
        self.total_agent_time_warnings = [0 for _ in agents]
        self.agent_timeout = False

        from io import StringIO
        self.agent_output = [StringIO() for _ in agents]

    def get_progress(self):
        if self.game_over:
            return 1.0
        else:
            return self.rules.get_progress(self)

    def _agent_crash(self, agent_index, quiet=False):
        if not quiet:
            traceback.print_exc()
        self.game_over = True
        self.agentCrashed = True
        self.rules.agent_crash(self, agent_index)

    OLD_STDOUT = None
    OLD_STDERR = None

    def mute(self, agent_index):
        if not self.mute_agents:
            return

        global OLD_STDOUT, OLD_STDERR
        OLD_STDOUT = sys.stdout
        OLD_STDERR = sys.stderr

        sys.stdout = self.agent_output[agent_index]
        sys.stderr = self.agent_output[agent_index]

    def unmute(self):
        if not self.mute_agents:
            return

        global OLD_STDOUT, OLD_STDERR
        sys.stdout = OLD_STDOUT
        sys.stderr = OLD_STDERR

    def run(self):
        self.display.initialize(self.state.data)
        self.num_moves = 0

        # self.display.initialize(self.state.makeObservation(1).data)

        # Inform learning agents of the game start.
        for i in range(len(self.agents)):
            agent = self.agents[i]
            if not agent:
                self.mute(i)
                sys.stderr.write("Agent %d failed to load" % i)
                self.unmute()
                self._agent_crash(i, quiet=True)
                return

            if "register_initial_state" in dir(agent):
                self.mute(i)
                if self.catch_exceptions:
                    try:
                        timed_func = TimeoutFunction(
                            agent.register_initial_state,
                            int(self.rules.get_max_startup_time(i))
                        )
                        try:
                            start_time = time.time()
                            timed_func(self.state.deep_copy())
                            time_taken = time.time() - start_time
                            self.total_agent_times[i] += time_taken
                        except TimeoutFunctionException:
                            sys.stderr.write("Agent %d ran out of time on startup!\n" % i)
                            self.unmute()
                            self.agent_timeout = True
                            self._agent_crash(i, quiet=True)
                            return
                    except Exception:
                        self._agent_crash(i, quiet=False)
                        self.unmute()
                        return
                else:
                    agent.register_initial_state(self.state.deep_copy())

                self.unmute()

        agent_index = self.starting_index
        num_agents = len(self.agents)

        while not self.game_over:
            # Fetch the next agent.
            agent = self.agents[agent_index]
            move_time = 0
            skip_action = False

            # Generate an observation of the state.
            if 'observation_function' in dir(agent):
                self.mute(agent_index)
                if self.catch_exceptions:
                    try:
                        timed_func = TimeoutFunction(agent.observation_function, int(self.rules.get_move_timeout(agent_index)))
                        try:
                            start_time = time.time()
                            observation = timed_func(self.state.deep_copy())
                        except TimeoutFunctionException:
                            skip_action = True
                        move_time += time.time() - start_time
                        self.unmute()
                    except Exception:
                        self._agent_crash(agent_index, quiet=False)
                        self.unmute()
                        return
                else:
                    observation = agent.observation_function(self.state.deep_copy())
                self.unmute()
            else:
                observation = self.state.deep_copy()

            # Solicit an action.
            action = None
            self.mute(agent_index)

            if self.catch_exceptions:
                try:
                    timed_func = TimeoutFunction(agent.get_action, int(self.rules.get_move_timeout(agent_index)) - int(move_time))
                    try:
                        start_time = time.time()
                        if skip_action:
                            raise TimeoutFunctionException()

                        action = timed_func(observation)
                    except TimeoutFunctionException:
                        sys.stderr.write("Agent %d timed out on a single move!\n" % agent_index)
                        self.agent_timeout = True
                        self._agent_crash(agent_index, quiet=True)
                        self.unmute()
                        return

                    move_time += time.time() - start_time

                    if move_time > self.rules.get_move_warning_time(agent_index):
                        self.total_agent_time_warnings[agent_index] += 1
                        sys.stderr.write("Agent %d took too long to make a move! This is warning %d\n" %
                                         (agent_index, self.total_agent_time_warnings[agent_index]))

                        if self.total_agent_time_warnings[agent_index] > self.rules.get_max_time_warnings(agent_index):
                            sys.stderr.write("Agent %d exceeded the maximum number of warnings: %d\n" %
                                             (agent_index, self.total_agent_time_warnings[agent_index]))
                            self.agent_timeout = True
                            self._agent_crash(agent_index, quiet=True)
                            self.unmute()
                            return

                    self.total_agent_times[agent_index] += move_time

                    if self.total_agent_times[agent_index] > self.rules.get_max_total_time(agent_index):
                        sys.stderr.write("Agent %d ran out of time! (time: %1.2f)\n" %
                                         (agent_index, self.total_agent_times[agent_index]))
                        self.agent_timeout = True
                        self._agent_crash(agent_index, quiet=True)
                        self.unmute()
                        return
                    self.unmute()
                except Exception as data:
                    self._agent_crash(agent_index)
                    self.unmute()
                    return
            else:
                action = agent.get_action(observation)

            self.unmute()

            # Execute the action.
            self.move_history.append((agent_index, action))

            if self.catch_exceptions:
                try:
                    self.state = self.state.generate_successor(agent_index, action)
                except Exception:
                    self.mute(agent_index)
                    self._agent_crash(agent_index)
                    self.unmute()
                    return
            else:
                self.state = self.state.generate_successor(agent_index, action)

            # Change the display.
            self.display.update(self.state.data)

            # idx = agentIndex - agentIndex % 2 + 1
            # self.display.update( self.state.makeObservation(idx).data )

            # Allow for game specific conditions (winning, losing, etc).
            self.rules.process(self.state, self)

            # Track progress.
            if agent_index == num_agents + 1:
                self.num_moves += 1

            # Next agent.
            agent_index = (agent_index + 1) % num_agents

            if _BOINC_ENABLED:
                boinc.set_fraction_done(self.get_progress())

        # Inform a learning agent of the game result.
        for agent_index, agent in enumerate(self.agents):
            if "final" in dir(agent):
                try:
                    self.mute(agent_index)
                    agent.final(self.state)
                    self.unmute()
                except Exception:
                    if not self.catch_exceptions:
                        raise
                    self._agent_crash(agent_index)
                    self.unmute()
                    return

        self.display.finish()
