import argparse
import math
import copy
from queue import PriorityQueue

parser = argparse.ArgumentParser()
parser.add_argument(
    '-f', '--file', help='Specify the input file. Defaults to input.txt')
parser.add_argument('-n', '--nvalue', type=int,
                    help='The puzzle size (3, 8, 15 etc). Defaults to 8. ')
args = parser.parse_args()

BOARD_SIZE = int(math.sqrt(args.nvalue + 1)) if args.nvalue else 3
INPUT_FILE = args.file if args.file else 'input.txt'


class Board:
    def __init__(self, grid, g, prev_boards):
        self.grid = grid
        self.g = g
        self.prev_boards = prev_boards
        self.f = self.g + self.h()

    def __lt__(self, other):
        return self.f < other.f

    def h(self):
        distance = 0
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                value = self.grid[row][column]
                row2 = math.floor((value - 1) / BOARD_SIZE)
                column2 = math.floor((value - 1) % BOARD_SIZE)
                distance += abs(row2 - row) + abs(column2 - column)
        return distance

    def generate_children(self):
        children = []
        adjacent_cordinates = []
        empty_cordinates = self.get_cordinates_for_value(BOARD_SIZE**2)
        empty_row = empty_cordinates[0]
        empty_column = empty_cordinates[1]

        if empty_row > 0:
            adjacent_cordinates.append([empty_row - 1, empty_column])

        if empty_row < BOARD_SIZE - 1:
            adjacent_cordinates.append([empty_row + 1, empty_column])

        if empty_column > 0:
            adjacent_cordinates.append([empty_row, empty_column - 1])

        if empty_column < BOARD_SIZE - 1:
            adjacent_cordinates.append([empty_row, empty_column + 1])

        for cordinate_pair in adjacent_cordinates:
            temp_grid = copy.deepcopy(self.grid)
            temp_grid[empty_row][empty_column] = temp_grid[cordinate_pair[0]
                                                           ][cordinate_pair[1]]
            temp_grid[cordinate_pair[0]][cordinate_pair[1]] = BOARD_SIZE**2

            child_prev_boards = copy.deepcopy(self.prev_boards)
            child_prev_boards.append(self.grid)
            children.append(Board(temp_grid, self.g + 1, child_prev_boards))
        return children

    def get_cordinates_for_value(self, value):
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                val = self.grid[row][column]
                if val == value:
                    return (row, column)

    def print_grids(self):
        grids = copy.deepcopy(self.prev_boards)
        grids.append(self.grid)
        for z in range(len(grids)):
            for y in range(BOARD_SIZE):
                value = grids[z][y]
                print(['E' if x == BOARD_SIZE**2 else str(x) for x in value])
            print()


def astar_solve(initial_grid):
    visited_grids = []
    children_queue = PriorityQueue()
    board = Board(initial_grid, 0, [])
    while not is_grid_solved(board.grid):
        children = board.generate_children()
        for child in children:
            if not has_been_visited(child.grid, visited_grids):
                children_queue.put((child.f, child))
        visited_grids.append(board.grid)
        board = children_queue.get()[1]
    return board


def count_inversions(grid):
    inversions = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            value = grid[row][col]
            if(value != BOARD_SIZE**2):
                # check current column
                for col2 in range(col + 1, BOARD_SIZE):
                    if value > grid[row][col2]:
                        inversions += 1
                # check following columns
                for col3 in range(0, BOARD_SIZE):
                    for row3 in range(row + 1, BOARD_SIZE):
                        if value > grid[row3][col3]:
                            inversions += 1
    return inversions


def is_solveable(grid):
    return count_inversions(grid) % 2 == 0


def is_grid_solved(grid):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            value = grid[row][col]
            if value != (row * BOARD_SIZE) + col + 1:
                return False
    return True


def has_been_visited(grid, visited_grids):
    return grid in visited_grids


def read_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()

    lines = [item for item in lines if item != '\n']

    board_count = lines[0]
    board_count = board_count.replace('\n', '')
    all_boards = []
    for i in range(int(board_count)):
        board = []
        for j in range(BOARD_SIZE):
            row = []
            line = lines[i * BOARD_SIZE + 1 + j]
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            for val in line:
                if val == 'E':
                    val = BOARD_SIZE**2
                row.append(int(val))
            board.append(row)
        all_boards.append(board)
    return all_boards


grids = read_file(INPUT_FILE)
i = 1
for grid in grids:
    print('Grid ' + str(i) + ':')
    if is_solveable(grid):
        board = astar_solve(grid)
        board.print_grids()
        print('Solveable: ' + str(count_inversions(grid)) + ' inversions')
        print('Number of moves: ' + str(board.g))
    else:
        print('Not solveable: ' + str(count_inversions(grid)) + ' inversions')
    print()
    i += 1
