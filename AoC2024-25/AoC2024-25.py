import time

from numpy.testing import assert_equal


def read_input(input_file: str) -> (list[list[int]], list[list[int]]):
    locks_and_keys = [lock_or_key.splitlines() for lock_or_key in open(input_file, 'r').read().split('\n\n')]
    keys = []
    locks = []
    for lock_or_key in locks_and_keys:
        if lock_or_key[0] == "#####":
            lock = [0] * 5
            for line in lock_or_key:
                for col, char in enumerate(line):
                    lock[col] += 1 if char == '#' else 0
            locks.append(lock)
        else:
            key = [7] * 5
            for line in lock_or_key:
                for col, char in enumerate(line):
                    key[col] -= 1 if char == '.' else 0
            keys.append(key)
    return locks, keys


def solve_part1(file_name: str) -> int:
    locks, keys = read_input(file_name)
    fits = 0
    for lock in locks:
        for key in keys:
            fit = True
            for col in range(0, 5):
                if key[col] + lock[col] > 7:
                    fit = False
                    break
            if fit:
                fits += 1
    return fits


def solve_part2(file_name: str) -> int:
    return 0


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 3360, 2: -1}

assert_equal(solve_part1('test1.txt'), 3, f'Incorrect answer to test')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')

solve_part(1)
