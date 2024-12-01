import numpy
from numpy.ma.testutils import assert_equal


def read_input(input_file):
    return numpy.array(
        list(zip(*[map(int, input_line.split()) for input_line in open(input_file, 'r').readlines()])))


def solve_part1(input_file):
    list_a, list_b = numpy.sort(read_input(input_file))
    return sum(abs(list_a - list_b))


def solve_part2(input_file):
    list_a, list_b = read_input(input_file)
    return sum(map(lambda a: a * numpy.count_nonzero(list_b == a), list_a))


assert_equal(solve_part1('test1.txt'), 11, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), 1189304, 'Incorrect answer to part 1.')
assert_equal(solve_part2('test1.txt'), 31, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), 24349736, 'Incorrect answer to part 2.')

print('Answer to part 1: ', solve_part1('input.txt'))
print('Answer to part 2: ', solve_part2('input.txt'))
