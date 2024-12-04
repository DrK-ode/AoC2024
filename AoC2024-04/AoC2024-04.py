import time

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
        return f'Matrix[{self._n_rows},{self._n_cols}]:\n {self._the_matrix_as_list}'

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


class Crawler:
    def __init__(self, matrix: Matrix, directions: list[(int, int)] = None, x: int = 0, y: int = 0):
        self._directions = matrix.all_directions() if directions is None else directions
        self._x = x
        self._y = y
        self._matrix = matrix

    def __str__(self):
        return f'Crawler@({self._x},{self._y})={self.at()}'

    def position(self):
        return self._x, self._y

    def go(self, direction: (int, int)) -> bool:
        x = self._x + direction[0]
        y = self._y + direction[1]
        if self._matrix.is_in_bound((x, y)):
            self._x = x
            self._y = y
            return True
        return False

    def directions(self) -> list[(int, int)]:
        return self._directions

    def go_named_direction(self, direction_name: str):
        self.go(self._matrix.direction_by_name(direction_name))
        return self.at()

    def at(self):
        return self._matrix[self._x, self._y]

    def set(self, x: int, y: int):
        self._x = x
        self._y = y


def search_location_for_sequence(word_search: Matrix, directions: list[(int, int)], x: int, y: int,
                                 sequence: list) -> int:
    if word_search[(x, y)] != sequence[0]:
        return 0
    words_found = 0
    crawler = Crawler(word_search, directions)
    for direction in crawler.directions():
        sequence_index = 1
        crawler.set(x, y)
        crawler.go(direction)
        while crawler.at() == sequence[sequence_index]:
            sequence_index += 1
            if sequence_index == len(sequence):
                words_found += 1
                break
            if not crawler.go(direction):
                break
    return words_found


def search_for_sequence(word_search: Matrix, sequence: list, directions: list[(int, int)]) -> int:
    words_found = 0
    for y in range(0, word_search.n_rows()):
        for x in range(0, word_search.n_cols()):
            words_found += search_location_for_sequence(word_search, directions, x, y, sequence)
    return words_found


def search_for_x(word_search: Matrix, sequence: list) -> int:
    x_found = 0
    for y in range(0, word_search.n_rows()):
        for x in range(0, word_search.n_cols()):
            x_found += search_location_for_x(word_search, x, y, sequence)
    return x_found


def search_location_for_x(word_search: Matrix, x: int, y: int, sequence: list) -> int:
    x_found = 0
    for direction in (1, 1), (-1, -1):
        if search_location_for_sequence(word_search, [direction], x, y, sequence):
            new_x = x + (len(sequence) - 1) * direction[0]
            diagonal = [(-direction[0], direction[1])]
            # Once the sequence is found along one diagonal there are two possible ways of forming an X
            if search_location_for_sequence(word_search, diagonal, new_x, y, sequence) or search_location_for_sequence(
                    word_search, diagonal, new_x, y, sequence[::-1]):
                x_found += 1
    return x_found


def solve_part1(input_file: str) -> int:
    word_search = Matrix(read_input(input_file))
    return search_for_sequence(word_search, ['X', 'M', 'A', 'S'], word_search.all_directions())


def solve_part2(input_file: str) -> int:
    word_search = Matrix(read_input(input_file))
    return search_for_x(word_search, ['M', 'A', 'S'])


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 2401, 2: 1822}
assert_equal(solve_part1('test1.txt'), 18, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test1.txt'), 9, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
