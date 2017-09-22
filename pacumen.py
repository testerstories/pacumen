from __future__ import print_function

import argparse
import logging
import textwrap

import os
import random
import sys

from game import layout
from rules.game_rules import GameRules

# Not referenced here; needed if "display moves" for text
# display is utilized.
from utilities import nearest_point


def parse_agent_args(arg_string):
    if arg_string is None:
        return {}

    pieces = arg_string.split(',')
    opts = {}

    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key, val = p, 1

        opts[key] = val

    return opts


def process_commands(argv):
    """
    Processes the command line used to run pacumen. The command line can
    contain a series of options which will determine how the pacman
    implementation executes.
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Pacumen Runner",
        epilog=textwrap.dedent(
            """
            USAGE:
                python pacumen.py <options>
                
            EXAMPLES:
                (1) python pacumen.py
                    - starts an interactive game
                (2) python pacumen.py --layout small_classic --zoom 2
                    - starts an interactive game on a smaller board, zoomed in
            """
        )
    )

    parser.add_argument("-v", "--verbose", dest="log_level", default="WARNING",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="increase output verbosity (default %(default)s)")

    parser.add_argument("-l", "--layout", dest="layout", default="medium_classic",
                        metavar='LAYOUT FILE',
                        help="provide a map LAYOUT FILE (default %(default)s)")

    parser.add_argument("-p", "--pacman", dest="pacman", default="KeyboardAgent",
                        metavar="TYPE",
                        help="the agent TYPE to use for Pac-Man (default %(default)s)")

    parser.add_argument("-g", "--ghosts", dest="ghost", default="RandomGhost",
                        metavar="TYPE",
                        help="the agent TYPE to use for the ghost(s) (default %(default)s)")

    parser.add_argument("-a", "--agentArgs", dest="agentArgs",
                        help='comma separated values sent to agent; e.g. "opt1=val1,opt2,opt3=val3"')

    parser.add_argument("-t", "--textGraphics", dest="textGraphics", default=False,
                        action="store_true",
                        help="display game output as text only (default %(default)s)")

    parser.add_argument("-q", "--quietTextGraphics", dest="quietGraphics", default=False,
                        action="store_true",
                        help="generate minimal output and no graphics (default %(default)s)")

    parser.add_argument("-z", "--zoom", dest="zoom", type=float, default=1.0,
                        help="control the size of the graphics window (default %(default)s)")

    parser.add_argument("-n", "--numGames", dest="numGames", type=int, default=1,
                        metavar="GAMES",
                        help="the number of GAMES to play (default %(default)s)")

    parser.add_argument("-k", "--numGhosts", dest="numGhosts", type=int, default=4,
                        help="the maximum number of ghosts to use (default %(default)s)")

    parser.add_argument("-x", "--numTraining", dest="numTraining", type=int, default=0,
                        help="number of training episodes (suppresses output); (default %(default)s)")

    parser.add_argument("--timeout", dest="timeout", type=int, default=30,
                        help="maximum time agents can spend computing in a single game (default %(default)s)")

    parser.add_argument("-f", "--fixRandomSeed", dest='fixRandomSeed', default=False,
                        action="store_true",
                        help="sets the random seed to always play the same game (default %(default)s)")

    parser.add_argument("--frameTime", dest="frameTime", type=float, default=0.1,
                        help="time to delay between frames; <0 means keyboard (default %(default)s)")

    parser.add_argument("-r", "--recordActions", dest="record", default=False,
                        action="store_true",
                        help="writes game histories to a file (named by timestamp) (default %(default)s)")

    parser.add_argument("--replay", dest="gameToReplay", default=None,
                        help="a recorded game file (pickle) to replay")

    parser.add_argument("-c", "--catchExceptions", dest='catchExceptions', default=False,
                        action='store_true',
                        help="turns on exception handling and timeouts during games (default %(default)s)")

    options = parser.parse_args(argv)

    logging.basicConfig(level=logging.getLevelName(options.log_level), format="%(message)s")

    args = dict()

    if options.fixRandomSeed:
        random.seed('cs188')

    args['layout'] = layout.get_layout(options.layout)

    if args['layout'] is None:
        raise Exception("The layout " + options.layout + " cannot be found")

    # Choose a Pacman agent.
    no_keyboard = options.gameToReplay is None and (options.textGraphics or options.quietGraphics)
    pacman_type = load_agent(options.pacman, no_keyboard)
    agent_opts = parse_agent_args(options.agentArgs)

    if options.numTraining > 0:
        args['numTraining'] = options.numTraining
        if 'numTraining' not in agent_opts:
            agent_opts['numTraining'] = options.numTraining

    pacman = pacman_type(**agent_opts)
    args['pacman'] = pacman

    # Don't display training games.
    if 'numTrain' in agent_opts:
        options.numQuiet = int(agent_opts['numTrain'])
        options.numIgnore = int(agent_opts['numTrain'])

    # Choose a ghost agent.
    ghost_type = load_agent(options.ghost, no_keyboard)
    args['ghosts'] = [ghost_type(i + 1) for i in range(options.numGhosts)]

    # Choose a display format.
    if options.quietGraphics:
        from displays import textual
        args['display'] = textual.NullGraphics()
    elif options.textGraphics:
        from displays import textual
        textual.SLEEP_TIME = options.frameTime
        args['display'] = textual.PacmanDisplay()
    else:
        from displays import graphical
        args['display'] = graphical.PacmanDisplay(options.zoom, frame_time=options.frameTime)

    args['numGames'] = options.numGames
    args['record'] = options.record
    args['catchExceptions'] = options.catchExceptions
    args['timeout'] = options.timeout

    # Special case: recorded games don't use the run_game method or args structure.
    if options.gameToReplay is not None:
        print('Replaying recorded game %s.' % options.gameToReplay)
        try:
            import cPickle as pickle
        except ImportError:
            import _pickle as pickle

        f = open(options.gameToReplay)

        try:
            recorded = pickle.load(f)
        finally:
            f.close()

        recorded['display'] = args['display']
        replay_game(**recorded)
        sys.exit(0)

    return args


def load_agent(pacman, no_graphics):
    python_path_string = os.path.expandvars("$PYTHONPATH")

    if python_path_string.find(';') == -1:
        python_path_dirs = python_path_string.split(':')
    else:
        python_path_dirs = python_path_string.split(';')

    python_path_dirs.append('.')

    for module_dir in python_path_dirs:
        if not os.path.isdir(module_dir):
            continue

        module_names = [f for f in os.listdir(module_dir) if f.startswith('agents_')]

        for module_name in module_names:
            try:
                agent_module = __import__(module_name[:-3])
            except ImportError:
                continue
            if pacman in dir(agent_module):
                if no_graphics and module_name == "agents_keyboard.py":
                    raise Exception("Using the keyboard requires graphics (not text display)")
                return getattr(agent_module, pacman)

    raise Exception("The agent " + pacman + " is not specified in any agents_*.py.")


def replay_game(layout, actions, display):
    import agents_pacman
    import agents_ghosts

    rules = GameRules()
    agents = [agents_pacman.GreedyAgent()] + [agents_ghosts.RandomGhost(i + 1) for i in range(layout.get_ghost_count())]
    game = rules.new_game(layout, agents[0], agents[1:], display)
    state = game.state
    display.initialize(state.data)

    for action in actions:
        # Execute the action
        state = state.generate_successor(*action)
        # Change the display
        display.update(state.data)
        # Allow for game specific conditions (winning, losing, etc.)
        rules.process(state, game)

    display.finish()


def run_game(layout, pacman, ghosts, display, numGames, record, numTraining=0, catchExceptions=False, timeout=30):
    import __main__
    __main__.__dict__['_display'] = display

    rules = GameRules(timeout)
    games = []

    for i in range(numGames):
        be_quiet = i < numTraining
        if be_quiet:
            # Suppress output and graphics.
            from displays import textual
            game_display = textual.NullGraphics()
            rules.quiet = True
        else:
            game_display = display
            rules.quiet = False

        game = rules.new_game(layout, pacman, ghosts, game_display, be_quiet, catchExceptions)
        game.run()

        if not be_quiet:
            games.append(game)

        if record:
            import time
            try:
                import cPickle as pickle
            except ImportError:
                import _pickle as pickle

            fname = ('recorded-game-%d' % (i + 1)) + '-'.join([str(t) for t in time.localtime()[1:6]])
            f = open(fname, 'wb')
            components = {'layout': layout, 'actions': game.move_history}
            pickle.dump(components, f)
            f.close()

    if (numGames - numTraining) > 0:
        scores = [game.state.get_score() for game in games]
        wins = [game.state.is_win() for game in games]
        win_rate = wins.count(True) / float(len(wins))
        print('Average Score:', sum(scores) / float(len(scores)))
        print('Scores:       ', ', '.join([str(score) for score in scores]))
        print('Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), win_rate))
        print('Record:       ', ', '.join([['Loss', 'Win'][int(w)] for w in wins]))

    return games

if __name__ == '__main__':
    kwargs = process_commands(sys.argv[1:])
    run_game(**kwargs)
