import time
from functools import cache

from numpy.testing import assert_equal


def read_input(input_file: str) -> (tuple[str], list[str]):
    lines = [line.rstrip() for line in open(input_file, 'r').readlines()]
    available_patterns = tuple([x.strip() for x in lines[0].split(',')])
    return available_patterns, lines[2:]


@cache
def match_variations(wanted_pattern: str, available_patterns: tuple[str], index: int = 0) -> int:
    if len(wanted_pattern) == index:
        return 1
    variations = 0
    for available_pattern in available_patterns:
        n = len(available_pattern)
        if wanted_pattern[index:index + n] == available_pattern:
            variations += match_variations(wanted_pattern, available_patterns, index + n)
        else:
            continue
    return variations


def solve_part1(file_name: str) -> int:
    available_patterns, wanted_patterns = read_input(file_name)
    possibles = 0
    for wanted_pattern in wanted_patterns:
        if match_variations(wanted_pattern, available_patterns) > 0:
            possibles += 1
    return possibles


def solve_part2(file_name: str) -> int:
    available_patterns, wanted_patterns = read_input(file_name)
    possibilities = 0
    for wanted_pattern in wanted_patterns:
        possibilities += match_variations(wanted_pattern, available_patterns)
    return possibilities


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 302, 2: 771745460576799}

# assert_equal(solve_part1('test1.txt'), 6, f'Incorrect answer to test')
# assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
# assert_equal(solve_part2('test1.txt'), 16, f'Incorrect answer to test')
# assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
