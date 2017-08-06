from __future__ import print_function

import search
import random


class EightPuzzleState:
    """
    This class defines the mechanics of the Eight Puzzle. The task of
    recasting this puzzle as a search problem is left to the class
    called EightPuzzleSearchProblem.
    """

    def __init__(self, numbers):
        """
        Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an instance
        of the eight puzzle. 0 represents the blank space. Thus, the list

        [1, 0, 2, 3, 4, 5, 6, 7, 8]

        represents the eight puzzle:

        -------------
        | 1 |   | 2 |
        -------------
        | 3 | 4 | 5 |
        -------------
        | 6 | 7 | 8 |
         ------------

        The configuration of the puzzle is stored in a 2-dimensional list
        (a list of lists) called 'cells'.
        """
        self.cells = []

        # A copy is made so as not to cause side-effects.
        numbers = numbers[:]
        numbers.reverse()

        for row in range(3):
            self.cells.append([])
            for col in range(3):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def is_goal(self):
        """
        Checks to see if the puzzle is in its goal state.

        -------------
        |   | 1 | 2 |
        -------------
        | 3 | 4 | 5 |
        -------------
        | 6 | 7 | 8 |
        -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).is_goal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).is_goal()
        False
        """
        current = 0
        for row in range(3):
            for col in range(3):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legal_moves(self):
        """
        Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legal_moves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation

        if row != 0:
            moves.append('up')
        if row != 2:
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 2:
            moves.append('right')

        return moves

    def result(self, move):
        """
        Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object. Instead,
        it returns a new object.
        """
        row, col = self.blankLocation

        if move == 'up':
            new_row = row - 1
            new_col = col
        elif move == 'down':
            new_row = row + 1
            new_col = col
        elif move == 'left':
            new_row = row
            new_col = col - 1
        elif move == 'right':
            new_row = row
            new_col = col + 1
        else:
            raise Exception("Illegal Move")

        # Create a copy of the current eightPuzzle.
        new_puzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        new_puzzle.cells = [values[:] for values in self.cells]

        # And update it to reflect the move
        new_puzzle.cells[row][col] = self.cells[new_row][new_col]
        new_puzzle.cells[new_row][new_col] = self.cells[row][col]
        new_puzzle.blankLocation = new_row, new_col

        return new_puzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
        Overloads '==' such that two eightPuzzles with the same configuration
        are equal.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
        True
        """
        for row in range(3):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __get_ascii_string(self):
        """
        Returns a display string for the maze
        """
        lines = []
        horizontal_line = ('-' * 13)
        lines.append(horizontal_line)

        for row in self.cells:
            row_line = '|'
            for col in row:
                if col == 0:
                    col = ' '
                row_line = row_line + ' ' + col.__str__() + ' |'
            lines.append(row_line)
            lines.append(horizontal_line)

        return '\n'.join(lines)

    def __str__(self):
        return self.__get_ascii_string()


# TODO: Implement the methods in this class.

class EightPuzzleSearchProblem(search.SearchProblem):
    """
    Implementation of a SearchProblem for the Eight Puzzle domain

    Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, puzzle):
        """
        Creates a new EightPuzzleSearchProblem which stores search
        information.
        """
        self.puzzle = puzzle

    def get_start_state(self):
        return puzzle

    def is_goal_state(self, state):
        return state.is_goal()

    def get_successors(self, state):
        """
        Returns list of (successor, action, stepCost) pairs where each
        successor is either left, right, up, or down from the original
        state and the cost is 1.0 for each.
        """
        successor = []
        for move in state.legal_moves():
            successor.append((state.result(move), move, 1))

        return successor

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        return len(actions)


EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]


def load_eight_puzzle(puzzle_number):
    """
    puzzleNumber: The number of the eight puzzle to load.

    Returns an eight puzzle object generated from one of the
    provided puzzles in EIGHT_PUZZLE_DATA.

    puzzleNumber can range from 0 to 5.

    >>> print(load_eight_puzzle(0))
    -------------
    | 1 |   | 2 |
    -------------
    | 3 | 4 | 5 |
    -------------
    | 6 | 7 | 8 |
    -------------
    """
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzle_number])


def create_random_eight_puzzle(moves=100):
    """
    moves: number of random moves to apply

    Creates a random eight puzzle by applying a series of 'moves',
    which are random moves to a solved puzzle.
    """
    puzzle = EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8])

    for move in range(moves):
        # Execute a random legal move.
        puzzle = puzzle.result(random.sample(puzzle.legal_moves(), 1)[0])

    return puzzle

if __name__ == '__main__':
    try:
        input = raw_input
    except NameError:
        pass

    puzzle = create_random_eight_puzzle(25)
    print('A random puzzle:')
    print(puzzle)

    problem = EightPuzzleSearchProblem(puzzle)
    path = search.breadth_first_search(problem)

    print('BFS found a path of %d moves: %s' % (len(path), str(path)))

    curr = puzzle
    i = 1

    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i > 1], a))
        print(curr)

        input("Press return for the next state...")
        i += 1
