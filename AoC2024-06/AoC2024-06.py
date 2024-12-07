import time

import numpy
from numpy.testing import assert_equal


def read_input(input_file: str) -> list[list[str]]:
    return [[character for character in line.rstrip()] for line in open(input_file, 'r').readlines()]


class Matrix:
    _directions = {'Right': (1, 0), 'UpRight': (1, -1), 'Up': (0, -1), 'UpLeft': (-1, -1), 'Left': (-1, 0),
                   'DownLeft': (-1, 1),
                   'Down': (0, 1), 'DownRight': (1, 1)}

    def __init__(self, src: list[list]):
        self._n_cols = len(src[0])
        self._n_rows = len(src)
        self._the_matrix_as_list = [elem for row in src for elem in row]

    def __str__(self):
        string = f'Matrix[{self._n_rows},{self._n_cols}]:'
        for r in range(0, self._n_rows):
            string += '\n' + ''.join(self.row(r))
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


def guard_itinerary(patrol_map: Matrix, starting_position: (int, int), starting_direction) -> [] or list[
    (int, int), (int, int)]:
    itinerary: [] or list[((int, int), (int, int))] = []
    guard = Crawler(patrol_map, starting_direction, starting_position)
    while guard.mark_step(itinerary):
        pass
    return itinerary


def solve_part1and2(input_file: str) -> (int, int):
    patrol_map = Matrix(read_input(input_file))
    starting_position = patrol_map.find('^')
    original_path = guard_itinerary(patrol_map, starting_position, patrol_map.direction_by_name('Up'))
    candidate_obstacles = set()
    for position, direction in original_path:
        candidate_obstacles.add((position[0], position[1]))
    candidate_obstacles.remove((starting_position[0], starting_position[1]))
    loop_obstacles = []
    tried = set()
    for index, obstacle in list(enumerate(original_path))[1:]:
        if obstacle[0] in tried:
            continue
        patrol_map[obstacle[0]] = '#'
        new_path = guard_itinerary(patrol_map, original_path[index - 1][0], original_path[index - 1][1])
        last_destination_x = new_path[-1][0][0] + new_path[-1][1][0]
        last_destination_y = new_path[-1][0][1] + new_path[-1][1][1]
        if patrol_map.is_in_bound((last_destination_x, last_destination_y)):
            loop_obstacles.append(obstacle)
        patrol_map[obstacle[0]] = '.'
        tried.add(obstacle[0])

    return len(candidate_obstacles) + 1, len(loop_obstacles)


def solve_parts() -> (int, int):
    duration = time.perf_counter()
    answer = solve_part1and2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part 1: {answer[0]}\nanswer to part 2: {answer[1]}\nfound in {duration:.2e} seconds')
    return answer


correct_answers = [5145, 1523]
assert_equal(solve_part1and2('test1.txt'), (41, 6), 'Incorrect answer to example.')
# assert_equal(solve_part1and2('input.txt'), correct_answers, f'Incorrect answer to part 1')

solve_parts()
