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


class Raindeer:
    def __init__(self, position: (int, int), direction: (int, int)):
        self.pos = position
        self.dir = direction
        self.score = 0

    def go_next(self):
        self.score += 1
        self.pos = self.next()

    def next(self) -> (int, int):
        return self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]

    def go_prev(self):
        self.score -= 1
        self.pos = self.prev()

    def prev(self) -> (int, int):
        return self.pos[0] - self.dir[0], self.pos[1] - self.dir[1]

    def state(self) -> ((int, int), (int, int)):
        return self.pos, self.dir

    def turn_left(self):
        self.score += 1000
        self.dir = (self.dir[1], -self.dir[0])

    def turn_right(self):
        self.score += 1000
        self.dir = (-self.dir[1], self.dir[0])

    def turn_back_right(self):
        self.score -= 1000
        self.dir = (self.dir[1], -self.dir[0])

    def turn_back_left(self):
        self.score -= 1000
        self.dir = (-self.dir[1], self.dir[0])


def descend_score(start_position: (int, int), scores: dict[((int, int), (int, int)), int]) -> int:
    raindeers = []
    for direction in Grid.EAST, Grid.WEST, Grid.NORTH, Grid.SOUTH:
        r = Raindeer(start_position, direction)
        if r.state() in scores:
            r.score = scores[r.state()]
            raindeers.append(r)
    tiles = set()
    tiles.add(raindeers[0].pos)
    while raindeers:
        raindeer = raindeers.pop()
        split = [raindeer, copy(raindeer), copy(raindeer), copy(raindeer)]
        split[1].turn_back_left()
        split[2].turn_back_right()
        split[3].turn_back_left()
        split[3].turn_back_left()
        for r in split:
            r.go_prev()
            score = scores.get(r.state(), None)
            if score is None or score > r.score:
                continue
            tiles.add(r.pos)
            if r.score > 0:
                raindeers.append(r)
    return len(tiles)


def solve_maze(maze: Grid) -> (int, dict[Raindeer, int]):
    winners = []
    raindeer = Raindeer(maze.find('S'), Grid.EAST)
    visited_states = {raindeer.state(): 0}
    candidate_raindeers: SortedList[Raindeer] = SortedList(key=lambda state: -state.score)
    candidate_raindeers.add(raindeer)
    while candidate_raindeers:
        next_states = []
        raindeer_forward = candidate_raindeers.pop()
        raindeer_left = copy(raindeer_forward)
        raindeer_left.turn_left()
        next_states.append(raindeer_left)
        raindeer_right = copy(raindeer_forward)
        raindeer_right.turn_right()
        next_states.append(raindeer_right)
        raindeer_forward.go_next()
        at_pos = maze[raindeer_forward.pos]
        if at_pos != '#':
            next_states.append(raindeer_forward)

        for raindeer in next_states:
            prev_score = visited_states.get(raindeer.state(), None)
            if prev_score is None or raindeer.score < prev_score:
                visited_states[raindeer.state()] = raindeer.score
                if maze[raindeer.pos] != 'E':
                    candidate_raindeers.add(raindeer)
                else:
                    winners.append(raindeer)
        if len(winners) > 0:
            # Remove all paths that does not have a lower score
            purge_index = candidate_raindeers.bisect_right(winners[0])
            for _ in range(0, purge_index):
                candidate_raindeers.pop(0)
    return winners[0].score, visited_states


def solve_part1(input_file: str) -> int:
    maze = Grid(read_input(input_file))
    return solve_maze(maze)[0]


def solve_part2(input_file: str) -> int:
    maze = Grid(read_input(input_file))
    _, states = solve_maze(maze)
    return descend_score(maze.find('E'), states)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 85420, 2: 492}

assert_equal(solve_part1('test1.txt'), 7036, 'Incorrect answer to example.')
assert_equal(solve_part1('test2.txt'), 11048, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test1.txt'), 45, 'Incorrect answer to example.')
assert_equal(solve_part2('test2.txt'), 64, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
