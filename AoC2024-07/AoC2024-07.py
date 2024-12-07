import time

import numpy
from numpy.testing import assert_equal


def read_input(input_file) -> list[(int, list[int])]:
    with open(input_file, 'r') as file:
        equations = []
        for line in file.readlines():
            test_result, numbers = line.split(':')
            numbers = list(map(int, numbers.split()))
            equations.append((int(test_result), numbers))
        return equations


def solve_part1(input_file: str) -> int:
    equations = read_input(input_file)
    result_sum = 0
    for result, numbers in equations:
        possibilities = numpy.array([numbers[0]])
        for number in numbers[1:]:
            additions = possibilities + number
            multiplications = possibilities * number
            possibilities = numpy.concatenate([additions, multiplications])
        result_sum += result if result in possibilities else 0
    return result_sum


def concat(n1: int, n2: int) -> int:
    return int(str(n1) + str(n2))


def solve_part2(input_file: str) -> int:
    equations = read_input(input_file)
    result_sum = 0
    for result, numbers in equations:
        possibilities = numpy.array([numbers[0]])
        for number in numbers[1:]:
            additions = possibilities + number
            multiplications = possibilities * number
            concatenations = [concat(possibility, number) for possibility in possibilities]
            possibilities = numpy.concatenate([additions, multiplications, concatenations])
        result_sum += result if result in possibilities else 0
    return result_sum


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 5837374519342, 2: 492383931650959}
assert_equal(solve_part1('test1.txt'), 3749, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test1.txt'), 11387, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
