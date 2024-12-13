import time

from numpy.testing import assert_equal
import regex


def read_input(input_file: str, p_extra: int = 0) -> list[((int, int), (int, int), (int, int))]:
    lines = [line.rstrip() for line in open(input_file, 'r').readlines()]
    index = 0
    machine_info = []
    while index < len(lines):
        a = [int(x) for x in regex.fullmatch(r'Button A: X\+(\d+), Y\+(\d+)', lines[index])[1:]]
        index += 1
        b = [int(x) for x in regex.fullmatch(r'Button B: X\+(\d+), Y\+(\d+)', lines[index])[1:]]
        index += 1
        p = [int(x) + p_extra for x in regex.fullmatch(r'Prize: X=(\d+), Y=(\d+)', lines[index])[1:]]
        index += 2
        machine_info.append((a, b, p))
    return machine_info


def least_tokens(machine_info) -> int:
    tokens = 0
    for (ax, ay), (bx, by), (px, py) in machine_info:
        divider = ax * by - bx * ay
        # Dependent equations
        if divider == 0:
            an_x, ar_x = divmod(px, ax)
            if ar_x != 0 or an_x < 0:
                continue
            an_y, ar_y = divmod(py, ay)
            if ar_y != 0 or an_y != an_x:
                continue
            bn_x, br_x = divmod(px, bx)
            if br_x != 0 or bn_x < 0:
                continue
            bn_y, br_y = divmod(px, bx)
            if br_y != 0 or bn_y != bn_x:
                continue
            tokens += min(3 * an_x, bn_x)
            continue
        an, ar = divmod(px * by - py * bx, divider)
        if ar != 0 or an < 0:
            continue
        bn, br = divmod(px - an * ax, bx)
        if br != 0 or bn < 0:
            continue
        tokens += 3 * an + bn
    return tokens


def solve_part1(input_file: str) -> int:
    machine_info = read_input(input_file)
    return least_tokens(machine_info)


def solve_part2(input_file: str) -> int:
    machine_info = read_input(input_file, 10000000000000)
    return least_tokens(machine_info)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 27157, 2: 104015411578548}

assert_equal(solve_part1('test1.txt'), 480, 'Incorrect answer to example.')
assert_equal(solve_part1('test2.txt'), 7, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
