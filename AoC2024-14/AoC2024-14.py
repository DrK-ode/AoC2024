import time

from numpy.ma.core import product
from numpy.testing import assert_equal
import regex


def read_input(input_file: str) -> list[(int, int, int, int)]:
    lines = [line.rstrip() for line in open(input_file, 'r').readlines()]
    robots = []
    for line in lines:
        robots.append([int(x) for x in regex.fullmatch(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)[1:]])
    return robots


def predict_positions(robots: list[(int, int, int, int)], time_in_seconds: int, room_width: int,
                      room_height: int) -> int:
    quadrants = [0, 0, 0, 0]
    for px, py, vx, vy in robots:
        px += vx * time_in_seconds
        py += vy * time_in_seconds
        px %= room_width
        py %= room_height
        px -= room_width // 2
        py -= room_height // 2
        if px == 0 or py == 0:
            continue
        q = 0
        if px < 0:
            q += 1
        if py < 0:
            q += 2
        quadrants[q] += 1
    return product(quadrants)


def inspect_positions(robots: list[(int, int, int, int)], period: int, offset: int, room_width: int, room_height: int):
    t = offset
    while True:
        picture = [['.'] * room_width for _ in range(0, room_height)]
        for robot_vectors in robots:
            px = (robot_vectors[0] + robot_vectors[2] * t) % room_width
            py = (robot_vectors[1] + robot_vectors[3] * t) % room_height
            picture[py][px] = '#'
        print(f'\nt = {t}')
        for line in picture:
            print(''.join(line))
        if input("Enter 's' to stop...") == 's':
            return t
        t += period


def solve_part1(input_file: str, width=101, height=103) -> int:
    robots = read_input(input_file)
    return predict_positions(robots, 100, width, height)


def solve_part2(input_file: str) -> int:
    robots = read_input(input_file)
    # The data has a period of 101 in x and 103 in y, respectively
    # The data shows clusters at t = 48 + nx*101 and t = 1 + ny*103
    # We seek the solution to the equation 101*nx - 103*ny = -47
    # 101 and 103 are both prime so the GCD is 1
    # Euclides algorithm:
    #   101 = 1*103 - 2
    #   103 = 51*2 + 1
    # i.e.
    #   1 = 103 - 51*2 = 103 - 51 * (103 - 101) = 101*51 - 103*50
    # Multiply by -47
    #   -47 = -47*101*51 + 47*103*50
    # One solution is:
    #   nx_0 = -2397
    #   ny_0 =  2350
    # All solutions are given by
    #   nx = nx_0 + 103*k
    #   ny = ny_0 - 101*k
    # Smallest non-negative nx is 75 so the smallest t is 48 + 75*101 = 7623
    return inspect_positions(robots, 103, 7623, 101, 103)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 222208000, 2: 7623}

assert_equal(solve_part1('test1.txt', 11, 7), 12, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

# for p in [1, 2]:
#    solve_part(p)
