import regex
import time

from numpy.testing import assert_equal


def read_input(input_file: str) -> str:
    return open(input_file, 'r').read()


def parse_mul(line_of_code: str) -> int:
    sum_of_mul = 0
    pattern = r"mul\([0-9]+,[0-9]+\)"
    for mul in regex.findall(pattern, line_of_code):
        x, y = regex.findall(r"[0-9]+", mul)
        sum_of_mul += int(x) * int(y)
    return sum_of_mul


def parse_mul_and_do(line_of_code: str) -> int:
    sum_of_mul = 0
    mul_enabled = True
    # regex.findall returns a list of all matches.
    # Each match is a list of the match of each group in the matching pattern.
    for match in regex.findall(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))", line_of_code):
        if len(match[0]) > 0:
            if mul_enabled:
                mul_match = regex.findall(r'mul\((\d+),(\d+)\)', match[0])
                x, y = mul_match[0]
                sum_of_mul += int(x) * int(y)
        elif len(match[1]) > 0:
            mul_enabled = True
        elif len(match[2]) > 0:
            mul_enabled = False
        else:
            raise Exception("Unknown match from regex.")
    return sum_of_mul


def solve_part1(input_file: str) -> int:
    code = read_input(input_file)
    return parse_mul(code)


def solve_part2(input_file: str) -> int:
    code = read_input(input_file)
    return parse_mul_and_do(code)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 183380722, 2: 82733683}
assert_equal(solve_part1('test1.txt'), 161, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test2.txt'), 48, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
