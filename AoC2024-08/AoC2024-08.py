import string
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
        the_string = f'Matrix[{self._n_rows},{self._n_cols}]:'
        for r in range(0, self._n_rows):
            the_string += '\n' + ''.join(self.row(r))
        return the_string

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
        index = -1
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


def find_antinodes_part1(antenna_locations: list[(int, int)]) -> list[(int, int)]:
    antinodes = []
    for i, location1 in enumerate(antenna_locations):
        for j in range(i + 1, len(antenna_locations)):
            location2 = antenna_locations[j]
            antinode = (2 * location1[0] - location2[0], 2 * location1[1] - location2[1])
            antinodes.append(antinode)
            antinode = (2 * location2[0] - location1[0], 2 * location2[1] - location1[1])
            antinodes.append(antinode)
    return antinodes


def solve_part1(input_file: str) -> int:
    the_map = Matrix(read_input(input_file))
    antinodes = set()
    for frequency in string.ascii_letters + string.digits:
        antenna_locations = the_map.find_all(frequency)
        for antinode in find_antinodes_part1(antenna_locations):
            if the_map.is_in_bound(antinode):
                antinodes.add(antinode)
    return len(antinodes)


def find_antinodes_part2(antenna_locations: list[(int, int)], width: int, height: int) -> list[(int, int)]:
    antinodes = []
    for i, location1 in enumerate(antenna_locations):
        for j in range(i + 1, len(antenna_locations)):
            location2 = antenna_locations[j]
            dx = location2[0] - location1[0]
            dy = location2[1] - location1[1]
            n = 0
            while True:
                antinode = (location1[0] + n * dx, location1[1] + n * dy)
                if 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                    antinodes.append(antinode)
                    n -= 1
                else:
                    break
            n = 1
            while True:
                antinode = (location1[0] + n * dx, location1[1] + n * dy)
                if 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                    antinodes.append(antinode)
                    n += 1
                else:
                    break
    return antinodes


def solve_part2(input_file: str) -> int:
    the_map = Matrix(read_input(input_file))
    antinodes = set()
    for frequency in string.ascii_letters + string.digits:
        antenna_locations = the_map.find_all(frequency)
        for antinode in find_antinodes_part2(antenna_locations, the_map.n_cols(), the_map.n_rows()):
            antinodes.add(antinode)
    return len(antinodes)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 271, 2: 994}

assert_equal(solve_part1('test1.txt'), 14, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test2.txt'), 9, 'Incorrect answer to example.')
assert_equal(solve_part2('test1.txt'), 34, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
