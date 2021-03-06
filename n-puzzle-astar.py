import argparse
import math
import copy
from queue import PriorityQueue
import time 

parser = argparse.ArgumentParser()
parser.add_argument(
    '-f', '--file', help='Specify the input file. Defaults to input.txt')
parser.add_argument('-n', '--nvalue', type=int,
                    help='The puzzle size (3, 8, 15 etc). Defaults to 8. ')
args = parser.parse_args()

BOARD_SIZE = int(math.sqrt(args.nvalue + 1)) if args.nvalue else 3
INPUT_FILE = args.file if args.file else 'input.txt'

class Board:
    def __init__(self, grid, move_list):
        self.grid = grid
        self.g = len(move_list)
        self.move_list = move_list
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
            child_prev_moves = copy.deepcopy(self.move_list)
            child_prev_moves.append(self.grid[cordinate_pair[0]][cordinate_pair[1]])
            children.append(Board(temp_grid, child_prev_moves))
        return children

    def get_cordinates_for_value(self, value):
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                val = self.grid[row][column]
                if val == value:
                    return (row, column)       

def is_board_solved(board):
    return board.f == board.g

def has_been_visited(grid, visited_grids):
    return grid in visited_grids

def astar_solve(initial_grid):
    visited_grids = []
    children_queue = PriorityQueue()
    board = Board(initial_grid, [])
    while not is_board_solved(board):
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
    inversion_count = count_inversions(grid)
    if inversion_count % 2 == 0:
        board = astar_solve(grid)
        print('Solveable: ' +str(inversion_count) + ' inversions')
        print('Moves: ' + str(board.move_list))
        print('Number of moves: ' + str(board.g))
    else:
        print('Not solveable: ' + str(inversion_count) + ' inversions')
    print()
    i += 1
print('Total execution time: ' + str(time.perf_counter()) + 'sec')
