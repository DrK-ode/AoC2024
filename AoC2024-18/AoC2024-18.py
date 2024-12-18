from copy import deepcopy
import time

import numpy
from sortedcontainers import SortedList
from numpy.testing import assert_equal


def read_input(input_file: str) -> (list[list[str]], list[str]):
    return [tuple(map(int, line.rstrip().split(','))) for line in open(input_file, 'r').readlines()]


class MemoryLocation:
    def __init__(self, start_addr: (int, int)):
        self.addr = numpy.array(start_addr)
        self.steps = 0

    def __getitem__(self, item):
        return self.addr[item]

    def __repr__(self):
        return f'addr: {self.addr}, steps: {self.steps}'

    def go(self, direction):
        self.addr += direction
        self.steps += 1

    def state(self) -> (int, int):
        return self.addr[0], self.addr[1]


def solve_maze(blocks: set[(int, int)], end_pos: (int, int) = (70, 70)) -> int:
    start_pos = (0, 0)
    start_addr = MemoryLocation(start_pos)
    visited = {start_addr.state(): start_addr.steps}
    candidates = SortedList(key=lambda state: -state.steps)
    candidates.add(start_addr)
    while candidates:
        addr = candidates.pop()
        for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            split_addr = deepcopy(addr)
            split_addr.go(direction)
            if (not 0 <= split_addr.addr[0] <= end_pos[0]) or (
                    not 0 <= split_addr.addr[1] <= end_pos[1]) or split_addr.state() in blocks:
                continue
            prev_steps = visited.get(split_addr.state(), -1)
            if prev_steps < 0 or split_addr.steps < prev_steps:
                visited[split_addr.state()] = split_addr.steps
                if split_addr.state() == end_pos:
                    return split_addr.steps
                candidates.add(split_addr)
    return -1


def solve_part1(input_file: str) -> int:
    block_list = read_input(input_file)[:1024]
    blocks = set()
    blocks.update(block_list)
    return solve_maze(blocks)


def solve_part2(input_file: str) -> str:
    block_list = read_input(input_file)
    lower_block_index = 0
    upper_block_index = len(block_list)
    while upper_block_index - lower_block_index > 1:
        middle = (lower_block_index + upper_block_index) // 2
        blocks = set()
        blocks.update(block_list[0:middle])
        steps = solve_maze(blocks)
        if steps < 0:
            upper_block_index = middle
        else:
            lower_block_index = middle
    return str(block_list[lower_block_index])


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 404, 2: '(27, 60)'}

assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
