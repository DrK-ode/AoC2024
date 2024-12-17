import time

from numpy.testing import assert_equal


def read_input(input_file: str) -> (list[int], list[int]):
    lines = [line.rstrip() for line in open(input_file, 'r').readlines()]
    registers = []
    for i in range(0, 3):
        registers.append(int(lines[i].split(':')[1].rstrip()))
    program = [int(x) for x in lines[-1].split(':')[1].rstrip().split(',')]
    return registers, program


def combo(operand: int, reg: list[int]) -> int:
    if 0 <= operand <= 3:
        return operand
    elif 4 <= operand <= 6:
        return reg[operand - 4]
    else:
        print(f'Invalid operand for combo op {operand}')


def execute_program(reg: list[int], prg: list[int], stop_at_first_output: bool = False) -> list[int]:
    instruction_ptr = 0
    prg_output = []
    while instruction_ptr < len(prg):
        op_code, operand = prg[instruction_ptr:instruction_ptr + 2]
        if op_code == 0:
            # adv
            reg[0] = reg[0] >> combo(operand, reg)
        elif op_code == 1:
            # bxl
            reg[1] ^= operand
        elif op_code == 2:
            # bst
            reg[1] = combo(operand, reg) % 8
        elif op_code == 3:
            # jnz
            if reg[0] > 0:
                instruction_ptr = operand
                continue
        elif op_code == 4:
            # bxc
            reg[1] ^= reg[2]
        elif op_code == 5:
            # out
            prg_output.append(combo(operand, reg) % 8)
            if stop_at_first_output:
                break
        elif op_code == 6:
            # bdv
            reg[1] = reg[0] >> combo(operand, reg)
        elif op_code == 7:
            # cdv
            reg[2] = reg[0] >> combo(operand, reg)
        else:
            raise Exception(f'Invalid Op-code: {op_code}')

        instruction_ptr += 2
    return prg_output


def solve_part1(input_file: str) -> str:
    reg, prg = read_input(input_file)
    prg_output = execute_program(reg, prg)
    return ','.join(map(str, prg_output))


def find_digits(prg, output_index: int, known_digits: int = 0) -> int or None:
    if output_index < 0:
        return known_digits
    candidate_reg_a = None
    known_digits = known_digits << 3
    for n in range(0, 8):
        reg_a = known_digits + n
        prg_output = execute_program([reg_a, 0, 0], prg, True)
        if prg_output[0] == prg[output_index]:
            reg_a = find_digits(prg, output_index - 1, reg_a)
            if reg_a is not None:
                if candidate_reg_a is None:
                    candidate_reg_a = reg_a
                else:
                    candidate_reg_a = min(candidate_reg_a, reg_a)
    if candidate_reg_a is None:
        return None
    return candidate_reg_a


def solve_part2(input_file: str) -> int:
    _, prg = read_input(input_file)
    reg_a = find_digits(prg, len(prg) - 1)
    return reg_a


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: '7,6,1,5,3,1,4,2,6', 2: 164541017976509}

assert_equal(solve_part1('test1.txt'), '4,6,3,5,6,3,5,2,1,0', 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test2.txt'), 117440, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
