import math
import time
from functools import cache

from numpy.testing import assert_equal


def read_input(input_file: str) -> list[int]:
    return [int(digit) for line in open(input_file, 'r').readlines() for digit in line.rstrip().split()]


def cut_in_two(stone: int) -> (int, int):
    digits = int(math.log10(stone) + 1)
    divider = math.pow(10, digits // 2)
    return stone // divider, stone % divider


@cache
def blink(blinks: int, stone: int) -> int:
    if blinks == 0:
        return 1
    if stone == 0:
        return blink(blinks - 1, 1)
    else:
        digits = int(math.log10(stone) + 1)
        if digits % 2 == 0:
            exponent = digits // 2
            divider = 1
            while exponent > 0:
                divider *= 10
                exponent -= 1
            return blink(blinks - 1, stone // divider) + blink(blinks - 1, stone % divider)
        else:
            return blink(blinks - 1, stone * 2024)


def count_stones(blinks: int, stones: list[int]) -> int:
    stone_dict = {}
    counter = 0
    for stone in stones:
        counter += blink(blinks, stone)
    return counter


def solve_part1(input_file: str) -> int:
    stones = read_input(input_file)
    return count_stones(25, stones)


def solve_part2(input_file: str) -> int:
    stones = read_input(input_file)
    return count_stones(75, stones)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 212655, 2: 253582809724830}

# Since return values are cached the timing will be off if the tests are run first
# assert_equal(solve_part1('test1.txt'), 55312, 'Incorrect answer to example.')
# assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
# assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

solve_part(1)
solve_part(2)
