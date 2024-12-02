import time

import numpy
from numpy.ma.testutils import assert_equal


def read_input(input_file: str) -> list[numpy.array]:
    return [numpy.array(list(map(int, input_line.split()))) for input_line in open(input_file, 'r').readlines()]


def is_report_safe(report: numpy.array, dampener: bool = False):
    return is_report_ascending_and_safe(report, dampener) or is_report_descending_and_safe(report, dampener)


def is_report_descending_and_safe(report: numpy.array, dampener: bool = False) -> bool:
    return is_report_ascending_and_safe(-report, dampener)


def is_report_ascending_and_safe(report: numpy.array, dampener: bool = False) -> bool:
    skip_next = False
    for i in range(0, len(report) - 1):
        if skip_next:
            skip_next = False
            continue
        diff = report[i + 1] - report[i]
        # Assume ascending
        if 0 < diff <= 3:
            continue
        if not dampener:
            return False
        dampener = False
        # dampen i+1 level
        if i + 2 == len(report) or 0 < report[i + 2] - report[i] <= 3:
            skip_next = True
            continue
        # dampen i level
        if i == 0 or 0 < report[i + 1] - report[i - 1] <= 3:
            continue
        return False
    return True


def solve_part1(input_file: str) -> int:
    reports = read_input(input_file)
    return list(map(is_report_safe, reports)).count(True)


def solve_part2(input_file: str) -> int:
    reports = read_input(input_file)
    return list(map(lambda r: is_report_safe(r, True), reports)).count(True)


def solve_part(part: int) -> int:
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


assert_equal(solve_part1('test1.txt'), 2, 'Incorrect answer to example.')
assert_equal(solve_part2('test1.txt'), 4, 'Incorrect answer to example.')

correct_answers = {1: 660, 2: 689}
for p in [1, 2]:
    assert_equal(solve_part(p), correct_answers[p], f'Incorrect answer to part {p}')
