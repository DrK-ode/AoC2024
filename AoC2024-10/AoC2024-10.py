import time

import numpy
from numpy.testing import assert_equal


def read_input(input_file: str) -> list[list[int]]:
    return [[int(digit) for digit in line.rstrip()] for line in open(input_file, 'r').readlines()]


class Matrix:
    _directions = {'Right': (1, 0), 'UpRight': (1, -1), 'Up': (0, -1), 'UpLeft': (-1, -1), 'Left': (-1, 0),
                   'DownLeft': (-1, 1),
                   'Down': (0, 1), 'DownRight': (1, 1)}

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

    @staticmethod
    def all_directions() -> list[(int, int)]:
        return list(Matrix._directions.values())

    @staticmethod
    def direction_by_name(name: str) -> (int, int):
        return Matrix._directions[name]

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
        x = index - y * self._n_rows
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
            x = index - y * self._n_rows
            results.append((x, y))

    def count(self, item):
        return self._the_matrix_as_list.count(item)


class Crawler:
    def __init__(self, matrix: Matrix, direction: (int, int), position: (int, int)):
        self._direction = numpy.array([direction[0], direction[1]])
        self._position = numpy.array([position[0], position[1]])
        self._matrix = matrix

    def __str__(self):
        return f'Crawler@({self._position})={self.at()}'

    def position(self) -> (int, int):
        return self._position[0], self._position[1]

    def mark_step(self, itinerary: [] or list[((int, int), (int, int))]) -> bool:
        item = ((self._position[0], self._position[1]), (self._direction[0], self._direction[1]))
        if item in itinerary:
            return False
        itinerary.append(item)
        at_next_position = self.next()
        if at_next_position is None:
            return False
        elif at_next_position == '#':
            self.turn()
        else:
            self._position += self._direction
        return True

    def turn(self):
        self._direction = self._direction.dot(numpy.array([[0, 1], [-1, 0]]))

    def next(self):
        next_position = self._position + self._direction
        if self._matrix.is_in_bound(next_position):
            return self._matrix[*next_position]
        else:
            return None

    def at(self):
        return self._matrix[self._position[0], self._position[1]]

    def set(self, x: int, y: int):
        self._position = numpy.array([x, y])


def solve_part1(input_file: str) -> (int, int):
    topo = Matrix(read_input(input_file), '!')
    trail = topo.find_all(0)
    score = 0
    for start in trail:
        steps = set()
        steps.add(start)
        for n in range(1, 10):
            next_steps = set()
            for x, y in steps:
                for next_position in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if topo[next_position] == n:
                        next_steps.add(next_position)
            steps = next_steps
        score += len(steps)
    return score


def solve_part2(input_file: str) -> (int, int):
    topo = Matrix(read_input(input_file), '!')
    trail = topo.find_all(0)
    score = 0
    for start in trail:
        steps = [start]
        for n in range(1, 10):
            next_steps = []
            for x, y in steps:
                for next_position in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if topo[next_position] == n:
                        next_steps.append(next_position)
            steps = next_steps
        score += len(steps)
    return score


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 786, 2: 1722}

assert_equal(solve_part1('test1.txt'), 36, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test1.txt'), 81, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
