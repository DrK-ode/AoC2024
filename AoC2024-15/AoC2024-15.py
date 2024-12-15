import time

import numpy
from PIL.ImageChops import offset
from numpy.testing import assert_equal


def read_input(input_file: str) -> (list[list[str]], list[str]):
    lines = [[character for character in line.rstrip()] for line in open(input_file, 'r').readlines()]
    warehouse = []
    moves = []
    fill_moves = False
    for line in lines:
        if len(line) == 0:
            fill_moves = True
        if fill_moves:
            moves.extend(line)
        else:
            warehouse.append(line)
    return warehouse, moves


class Matrix:
    def __init__(self, src: list[list], border=None):
        if border is not None:
            for line in src:
                line.insert(0, border)
                line.append(border)
            src.insert(0, [border] * len(src[0]))
            src.append([border] * len(src[0]))
        self._n_cols = len(src[0])
        self._n_rows = len(src)
        self._the_matrix_as_list = [elem for row in src for elem in row]

    def __str__(self):
        string = f'Matrix[{self._n_rows},{self._n_cols}]:'
        for r in range(0, self._n_rows):
            string += '\n' + ''.join(map(str, self.row(r)))
        return string

    def row(self, y: int) -> list:
        return self._the_matrix_as_list[y * self._n_cols:(y + 1) * self._n_cols]

    def n_rows(self) -> int:
        return self._n_rows

    def col(self, x: int) -> list:
        return self._the_matrix_as_list[x::self._n_cols]

    def n_cols(self) -> int:
        return self._n_cols

    def __getitem__(self, key: (int, int)):
        return self._the_matrix_as_list[key[0] + key[1] * self._n_cols]

    def __setitem__(self, key: (int, int), value):
        self._the_matrix_as_list[key[0] + key[1] * self._n_cols] = value

    def is_in_bound(self, key: (int, int)) -> bool:
        return 0 <= key[0] < self._n_cols and 0 <= key[1] < self._n_rows

    def find(self, item) -> (int, int):
        index = self._the_matrix_as_list.index(item)
        y = index // self._n_cols
        x = index % self._n_cols
        return x, y

    def find_all(self, item) -> list:
        results = []
        index = 0
        while True:
            try:
                index = self._the_matrix_as_list.index(item, index + 1)
            except ValueError:
                return results
            y = index // self._n_cols
            x = index % self._n_cols
            results.append((x, y))

    def count(self, item):
        return self._the_matrix_as_list.count(item)


def widen(warehouse: list[list[str]]) -> list[list[str]]:
    wide_warehouse = []
    for line in warehouse:
        wide_line = []
        for item in line:
            if item == '.' or item == '#':
                wide_line.append(item)
                wide_line.append(item)
            elif item == 'O':
                wide_line.append('[')
                wide_line.append(']')
            else:
                wide_line.append('@')
                wide_line.append('.')
        wide_warehouse.append(wide_line)
    return wide_warehouse


def move_small_box(warehouse: Matrix, box_position: numpy.array, direction: (int, int)) -> bool:
    destination = box_position + direction
    while True:
        at_destination = warehouse[destination]
        if at_destination == 'O':
            destination += direction
            continue
        if at_destination == '#':
            return False
        warehouse[destination] = 'O'
        warehouse[box_position] = '.'
        return True


def move_large_box(warehouse: Matrix, box_position: numpy.array, direction: (int, int)) -> bool:
    if direction[0] == 0:
        left_edge = box_position if warehouse[box_position] == '[' else box_position + (-1, 0)
        return move_large_box_vertically(warehouse, left_edge, direction)
    else:
        return move_large_box_horizontally(warehouse, box_position, direction)


def move_large_box_vertically(warehouse: Matrix, og_left_box_edge: numpy.array, direction: (int, int)) -> bool:
    all_boxes = [[og_left_box_edge]]
    while True:
        next_generation = []
        for left_box_edge in all_boxes[-1]:
            left_destination = left_box_edge + direction
            at_left = warehouse[left_destination]
            at_right = warehouse[left_destination + (1, 0)]
            if at_left == '#' or at_right == '#':
                return False
            if at_left == '.' and at_right == '.':
                continue
            if at_right == '[':
                next_generation.append(left_destination + (1, 0))
            if at_left == '[':
                next_generation.append(left_destination)
            elif at_left == ']':
                next_generation.append(left_destination + (-1, 0))
        if len(next_generation) == 0:
            break
        all_boxes.append(next_generation)
    for boxes in reversed(all_boxes):
        for left_box_edge in boxes:
            left_destination = left_box_edge + direction
            warehouse[left_destination] = '['
            warehouse[left_destination + (1, 0)] = ']'
            warehouse[left_box_edge] = '.'
            warehouse[left_box_edge + (1, 0)] = '.'
    return True


def move_large_box_horizontally(warehouse: Matrix, box_position: numpy.array, direction: (int, int)) -> bool:
    destination = box_position + direction
    while True:
        at_destination = warehouse[destination]
        if at_destination == '[' or at_destination == ']':
            destination += direction
            continue
        if at_destination == '#':
            return False
        # Pushing large box
        while not numpy.array_equal(destination, box_position):
            warehouse[destination] = warehouse[destination - direction]
            destination -= direction
        warehouse[box_position] = '.'
        return True


def move_robot(warehouse: Matrix, robot: numpy.array, direction: (int, int)):
    destination = robot + direction
    at_destination = warehouse[destination]
    if at_destination == '#':
        return
    if at_destination == '.':
        robot += direction
        return
    # Robot is moving into a box
    if at_destination == 'O':
        if move_small_box(warehouse, destination, direction):
            robot += direction
    else:
        if move_large_box(warehouse, destination, direction):
            robot += direction


def move_around(warehouse: Matrix, moves: list[str]):
    robot = numpy.array(warehouse.find('@'))
    warehouse[robot] = '.'
    for i, robot_move in enumerate(moves):
        if robot_move == '>':
            move_robot(warehouse, robot, (1, 0))
        elif robot_move == '^':
            move_robot(warehouse, robot, (0, -1))
        elif robot_move == '<':
            move_robot(warehouse, robot, (-1, 0))
        elif robot_move == 'v':
            move_robot(warehouse, robot, (0, 1))
    warehouse[robot] = '@'


def gps_sum(warehouse: Matrix, item: str) -> int:
    box_sum = 0
    for box in warehouse.find_all(item):
        box_sum += box[0] + 100 * box[1]
    return box_sum


def solve_part1(input_file: str) -> int:
    warehouse, moves = read_input(input_file)
    warehouse = Matrix(warehouse)
    move_around(warehouse, moves)
    return gps_sum(warehouse, 'O')


def solve_part2(input_file: str) -> int:
    warehouse, moves = read_input(input_file)
    warehouse = widen(warehouse)
    warehouse = Matrix(warehouse)
    move_around(warehouse, moves)
    return gps_sum(warehouse, '[')


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 1514333, 2: 1528453}

assert_equal(solve_part1('test1.txt'), 2028, 'Incorrect answer to example.')
assert_equal(solve_part1('test2.txt'), 10092, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test3.txt'), 618, 'Incorrect answer to example.')
assert_equal(solve_part2('test2.txt'), 9021, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
