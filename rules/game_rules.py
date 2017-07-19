from game.game import Game
from game.game_state import GameState


class GameRules:
    def __init__(self, timeout=30):
        self.timeout = timeout

    def new_game(self, layout, pacman_agent, ghost_agents, display, quiet=False, catch_exceptions=False):
        agents = [pacman_agent] + ghost_agents[:layout.get_ghost_count()]
        init_state = GameState()
        init_state.initialize(layout, len(ghost_agents))
        game = Game(agents, display, self, catch_exceptions=catch_exceptions)
        game.state = init_state
        self.initial_state = init_state.deep_copy()
        self.quiet = quiet
        return game

    def process(self, state, game):
        if state.is_win():
            self.win(state, game)
        if state.is_lose():
            self.lose(state, game)

    def win(self, state, game):
        if not self.quiet:
            print("Pac-Man emerges victorious! Score: %d" % state.data.score)

        game.game_over = True

    def lose(self, state, game):
        if not self.quiet:
            print("Pac-Man died! Score: %d" % state.data.score)

        game.game_over = True

    def get_progress(self, game):
        return float(game.state.get_num_food()) / self.initial_state.get_num_food()

    def agent_crash(self, game, agent_index):
        if agent_index == 0:
            print("Pac-Man crashed")
        else:
            print("A ghost crashed")

    def get_max_total_time(self, agent_index):
        return self.timeout

    def get_max_startup_time(self, agent_index):
        return self.timeout

    def get_move_warning_time(self, agent_index):
        return self.timeout

    def get_move_timeout(self, agent_index):
        return self.timeout

    def get_max_time_warnings(self, agent_index):
        return 0
