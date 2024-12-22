import time
from functools import cache

from numpy.testing import assert_equal


def read_input(input_file: str) -> list[str]:
    return [line.rstrip() for line in open(input_file, 'r').readlines()]


@cache
def from_key_to_pressed_key(is_numpad: bool, from_key: str, to_key: str) -> str:
    key_positions = from_key_to_pressed_key.numpad_key_positions if is_numpad else from_key_to_pressed_key.dirpad_key_positions
    from_x, from_y = key_positions[from_key]
    to_x, to_y = key_positions[to_key]
    delta_x = to_x - from_x
    delta_y = to_y - from_y
    movements = []
    danger_y = 0 if is_numpad else 1
    # Avoid gap when going to/from leftmost/bottom column/row
    # Prefer going horizontally if going left
    # Prefer going vertically if going right
    if (to_x == 0 and from_y == danger_y) or (not (from_x == 0 and to_y == danger_y) and delta_x > 0):
        for y_move in range(0, abs(delta_y)):
            movements.append('^' if delta_y > 0 else 'v')
        for x_move in range(0, abs(delta_x)):
            movements.append('>' if delta_x > 0 else '<')
    else:
        for x_move in range(0, abs(delta_x)):
            movements.append('>' if delta_x > 0 else '<')
        for y_move in range(0, abs(delta_y)):
            movements.append('^' if delta_y > 0 else 'v')
    movements.append('A')
    return ''.join(movements)


from_key_to_pressed_key.numpad_key_positions = {
    '7': (0, 3), '8': (1, 3), '9': (2, 3),
    '4': (0, 2), '5': (1, 2), '6': (2, 2),
    '1': (0, 1), '2': (1, 1), '3': (2, 1),
    '0': (1, 0), 'A': (2, 0)}
from_key_to_pressed_key.dirpad_key_positions = {'^': (1, 1), 'A': (2, 1), '<': (0, 0), 'v': (1, 0), '>': (2, 0)}


@cache
def count_presses_for_key(from_key: str, to_key: str, level: int, initial_call=True):
    if level == 0:
        return 1
    key_presses = 0
    current_key = 'A'
    for key in from_key_to_pressed_key(initial_call, from_key, to_key):
        key_presses += count_presses_for_key(current_key, key, level - 1, False)
        current_key = key
    return key_presses


def calc_codes(codes: list[str], number_of_robots: int) -> int:
    complexity_sum = 0
    for code in codes:
        total_presses = 0
        current_key = 'A'
        for key in code:
            presses = count_presses_for_key(current_key, key, number_of_robots)
            current_key = key
            total_presses += presses
        numeric_part = int(code[:-1])
        complexity_sum += total_presses * numeric_part
    return complexity_sum


def solve_part1(file_name: str) -> int:
    codes = read_input(file_name)
    return calc_codes(codes, 3)


def solve_part2(file_name: str) -> int:
    codes = read_input(file_name)
    return calc_codes(codes, 26)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 109758, 2: 134341709499296}

# assert_equal(solve_part1('test1.txt'), 126384, f'Incorrect answer to test')
# assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
# assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
