from copy import copy
import time

from sortedcontainers import SortedList
from numpy.testing import assert_equal


def read_input(input_file: str) -> (list[list[str]], list[str]):
    return [[character for character in line.rstrip()] for line in open(input_file, 'r').readlines()]


class Grid:
    EAST = (1, 0)
    WEST = (-1, 0)
    NORTH = (0, -1)
    SOUTH = (0, 1)
    NORTH_EAST = (1, -1)
    NORTH_WEST = (-1, -1)
    SOUTH_EAST = (1, 1)
    SOUTH_WEST = (-1, 1)

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


class Racer:
    def __init__(self, position: (int, int), direction: (int, int)):
        self.position = position
        self.time = 0

    def go(self, direction: (int, int)):
        self.time += 1
        self.position = self.position[0] + direction[0], self.position[1] + direction[1]


def solve_maze(maze: Grid, from_token: str, to_token: str, obstacle_token: str) -> (
        dict[(int, int), int], dict[(int, int), int]):
    initial_racer = Racer(maze.find(from_token), Grid.EAST)
    visited_states = {initial_racer.position: initial_racer.time}
    candidate_racers: SortedList[Racer] = SortedList(key=lambda r: -r.time)
    candidate_racers.add(initial_racer)
    while candidate_racers:
        racer = candidate_racers.pop()

        for direction in (Grid.EAST, Grid.NORTH, Grid.WEST, Grid.SOUTH):
            split_racer = copy(racer)
            split_racer.go(direction)
            at_pos = maze[split_racer.position]
            if at_pos == obstacle_token:
                continue
            prev_time = visited_states.get(split_racer.position, -1)
            if prev_time < 0 or split_racer.time < prev_time:
                visited_states[split_racer.position] = split_racer.time
                if at_pos != to_token:
                    candidate_racers.add(split_racer)
    return visited_states


class Cheat:
    def __init__(self, start_position, end_position, savings):
        self.start_position = start_position
        self.end_position = end_position
        self.savings = savings

    def __repr__(self):
        return f'Cheat: {self.start_position}->{self.end_position} saves {self.savings} ps'


def find_number_of_cheats(maze: Grid, fw_times: dict[(int, int), int], bw_times: dict[(int, int), int], cheat_time: int,
                          min_savings: int) -> int:
    best_non_cheat_time = fw_times[maze.find('E')]
    number_of_cheats = 0
    for cheat_start_x in range(1, maze.n_cols() - 1):
        for cheat_start_y in range(1, maze.n_rows() - 1):
            cheat_start = cheat_start_x, cheat_start_y
            if maze[cheat_start] == '#' or cheat_start not in fw_times:
                continue
            for delta_x in range(-cheat_time, cheat_time + 1):
                time_left_for_y = cheat_time - abs(delta_x)
                for delta_y in range(-time_left_for_y, time_left_for_y + 1):
                    cheat_end = cheat_start[0] + delta_x, cheat_start[1] + delta_y
                    if cheat_end[0] <= 0 or maze.n_cols() - 1 <= cheat_end[0] or cheat_end[
                        1] <= 0 or maze.n_rows() - 1 <= cheat_end[1] or maze[
                        cheat_end] == '#' or cheat_end not in bw_times:
                        continue
                    steps = fw_times[cheat_start] + bw_times[cheat_end] + abs(delta_x) + abs(delta_y)
                    savings = best_non_cheat_time - steps
                    if savings >= min_savings:
                        number_of_cheats += 1
    return number_of_cheats


def count_cheats(file_name: str, cheat_time: int, min_savings: int) -> int:
    maze = Grid(read_input(file_name))
    forward_steps = solve_maze(maze, 'S', 'E', '#')
    backward_steps = solve_maze(maze, 'E', 'S', '#')
    return find_number_of_cheats(maze, forward_steps, backward_steps, cheat_time, min_savings)


def solve_part1(file_name: str) -> int:
    return count_cheats(file_name, 2, 100)


def solve_part2(file_name: str) -> int:
    return count_cheats(file_name, 20, 100)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 1346, 2: 985482}

assert_equal(count_cheats('test1.txt', 2, 12), 8, f'Incorrect answer to test')
assert_equal(count_cheats('test1.txt', 20, 50), 285, f'Incorrect answer to test')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
