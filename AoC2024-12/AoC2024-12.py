import time

from numpy.testing import assert_equal
from samba.netcmd.user import cmd_user_rename


def read_input(input_file: str) -> list[list[(str, bool)]]:
    return [[[character, False] for character in line.rstrip()] for line in open(input_file, 'r').readlines()]


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


def find_neighbours_and_circumference(garden: Matrix, location: (int, int), plant: str, region: list[(int, int)]):
    x, y = location
    circumference = 0
    for next_location in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        next_plot = garden[next_location]
        if next_plot[0] != plant:
            circumference += 1
            continue
        if next_plot[1]:
            continue
        region.append(next_location)
        next_plot[1] = True
        circumference += find_neighbours_and_circumference(garden, next_location, plant, region)
    return circumference


def find_neighbours(garden: Matrix, location: (int, int), plant: str, region: list[(int, int)]):
    x, y = location
    for next_location in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        next_plot = garden[next_location]
        if next_plot[0] != plant or next_plot[1]:
            continue
        region.append(next_location)
        next_plot[1] = True
        find_neighbours_and_circumference(garden, next_location, plant, region)


def calculate_sides(garden: Matrix, region: list[(int, int)], plant: str) -> int:
    corners = 0
    for x, y in region:
        east_plant = garden[x + 1, y][0]
        west_plant = garden[x - 1, y][0]
        north_plant = garden[x, y + 1][0]
        south_plant = garden[x, y - 1][0]
        northeast_plant = garden[x + 1, y + 1][0]
        northwest_plant = garden[x - 1, y + 1][0]
        southeast_plant = garden[x + 1, y - 1][0]
        southwest_plant = garden[x - 1, y - 1][0]
        # NE outer
        if north_plant != plant and east_plant != plant:
            corners += 1
        # NW outer
        if north_plant != plant and west_plant != plant:
            corners += 1
        # SE outer
        if south_plant != plant and east_plant != plant:
            corners += 1
        # SW outer
        if south_plant != plant and west_plant != plant:
            corners += 1
        # NE inner
        if southwest_plant != plant and south_plant == plant and west_plant == plant:
            corners += 1
        # NW inner
        if southeast_plant != plant and south_plant == plant and east_plant == plant:
            corners += 1
        # SE inner
        if northwest_plant != plant and north_plant == plant and west_plant == plant:
            corners += 1
        # SW inner
        if northeast_plant != plant and north_plant == plant and east_plant == plant:
            corners += 1
    return corners


def solve_part1(input_file: str) -> int:
    garden = Matrix(read_input(input_file), ['!', True])
    return fence_price(garden)


def fence_price(garden: Matrix, discount: bool = False) -> int:
    total_fence_price = 0
    for y in range(1, garden.n_rows() - 1):
        for x in range(1, garden.n_cols() - 1):
            location = (x, y)
            current_plot = garden[location]
            if current_plot[1]:
                continue
            current_plot[1] = True
            region = [location]
            if discount:
                find_neighbours(garden, location, current_plot[0], region)
                sides = calculate_sides(garden, region, current_plot[0])
                total_fence_price += sides * len(region)
            else:
                circumference = find_neighbours_and_circumference(garden, location, current_plot[0], region)
                total_fence_price += circumference * len(region)
    return total_fence_price


def solve_part2(input_file: str) -> int:
    garden = Matrix(read_input(input_file), ['!', True])
    return fence_price(garden, True)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 1375476, 2: 821372}

assert_equal(solve_part1('test1.txt'), 1930, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test2.txt'), 236, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
