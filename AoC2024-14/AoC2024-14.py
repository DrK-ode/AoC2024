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


def inspect_positions(robots: list[(int, int, int, int)], period: int, offset: int):
    height = 103
    width = 101
    t = offset
    while True:
        picture = [['.'] * width for _ in range(0, height)]
        for robot_vectors in robots:
            px = (robot_vectors[0] + robot_vectors[2] * t) % width
            py = (robot_vectors[1] + robot_vectors[3] * t) % height
            picture[py][px] = '#'
        print(f'\nt = {t}')
        for line in picture:
            print(''.join(line))
        if input("Enter 's' to stop...") == 's':
            return t
        t += period


def calc_positions(robots: list[(int, int, int, int)], t: int) -> list[(int, int)]:
    height = 103
    width = 101
    positions = []
    for rv in robots:
        positions.append(((rv[0] + rv[2] * t) % width, (rv[1] + rv[3] * t) % height))
    return positions


def calc_scores(positions: list[(int, int)]) -> (int, int):
    v_scores = [0] * 101
    h_scores = [0] * 103
    for pos in positions:
        v_scores[pos[0]] += 1
        h_scores[pos[1]] += 1
    return max(h_scores), max(v_scores)


def find_offsets(robots: list[(int, int, int, int)]) -> (int, int):
    h_best_score = (0, None)
    v_best_score = (0, None)
    for t in range(0, 103):
        positions = calc_positions(robots, t)
        h_score, v_score = calc_scores(positions)
        if h_score > h_best_score[0]:
            h_best_score = (h_score, t)
        if v_score > v_best_score[0]:
            v_best_score = (v_score, t)
    return v_best_score[1], h_best_score[1]


def print_positions(positions):
    robot_map = [[' '] * 101 for _ in range(0, 103)]
    for pos in positions:
        robot_map[pos[1]][pos[0]] = '#'
    for line in robot_map:
        print(''.join(line))


def print_tree_from_file(file_name: str, generation: int):
    robots = read_input(file_name)
    print_positions(calc_positions(robots, generation))
    return


def solve_part1(input_file: str, width=101, height=103) -> int:
    robots = read_input(input_file)
    return predict_positions(robots, 100, width, height)


def solve_part2(input_file: str, manually=False) -> int:
    robots = read_input(input_file)
    if manually:
        return inspect_positions(robots, 103, 0)
    # The data has a period of 101 in x and 103 in y, respectively.
    # The data shows clusters at
    delta_x, delta_y = find_offsets(robots)
    # We seek the solution to the equations
    #   t = delta_x + nx*101
    #   t = delta_y + ny*103.
    # i.e.
    #   101*nx - 103*ny = delta_y - delta_x = delta_n.
    delta_n = delta_y - delta_x
    # Since 101 and 103 are both prime the GCD is 1.
    # Euclides algorithm:
    #   101 = 1*103 - 2
    #   103 = 51*2 + 1
    #   101 - 1*103 = 2
    #   103 - 51*2 = 1
    # i.e.
    #   1 = 103 - 51*2 = 103 - 51 * (103 - 101) = 101*51 - 103*50.
    # Multiply by delta_n
    #   delta_n = 101*delta_n*51 - 103*delta_n*50
    # One solution is trivially:
    #   nx_0 = 51*delta_n
    #   ny_0 = 50*delta_n
    nx = delta_n * 51
    # All solutions are given by
    #   nx = nx_0 + 103*k
    #   ny = ny_0 + 101*k
    # Smallest non-negative nx is yields the smallest t = delta_x + nx * 101
    nx -= 103 * (nx // 103)
    t = delta_x + nx * 101
    # print_positions(calc_positions(robots, t))
    return t


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
assert_equal(solve_part2('other_input.txt'), 2241, f'Incorrect answer to part 2')
assert_equal(solve_part2('another_input.txt'), 42, f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)

print_tree_from_file('input.txt', correct_answers[2])
