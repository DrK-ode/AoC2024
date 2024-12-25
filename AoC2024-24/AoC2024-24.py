import re
import time
from copy import copy

from numpy.testing import assert_equal


def and_op(a: int, b: int) -> int:
    return a & b


def or_op(a: int, b: int) -> int:
    return a | b


def xor_op(a: int, b: int) -> int:
    return a ^ b


class Value:
    def __init__(self, name, value: int or None = None, op: str or None = None):
        self.name = name
        self.value = value
        if op is None:
            self.op = None
        elif op == 'AND':
            self.op = and_op
        elif op == 'OR':
            self.op = or_op
        elif op == 'XOR':
            self.op = xor_op
        else:
            raise Exception(f'Invalid operator: {op}')
        self.inputs = []

    def __repr__(self):
        return f'{self.name}'

    def __lt__(self, other):
        return self.name < other.name

    def calc(self):
        if self.op is not None:
            self.value = self.op(*[inp.value for inp in self.inputs])

    def dependencies(self, deps=None) -> set:
        if deps is None:
            deps = set()
        deps.add(self)
        for dep in self.inputs:
            dep.dependencies(deps)
        return deps


def read_input(input_file: str) -> ((list[Value], list[Value]), list[Value], dict[str, Value]):
    initial_wires, gate_connections = [lines.splitlines() for lines in open(input_file, 'r').read().split('\n\n')]

    values: dict[str, Value] = {}
    input_values = [[], []]
    output_values = []

    pattern = r'(...): (\d)'
    for initial_wire in initial_wires:
        matches = re.fullmatch(pattern, initial_wire)
        input_value = Value(matches[1], value=int(matches[2]))
        values[matches[1]] = input_value
        if input_value.name.startswith('x'):
            input_values[0].append(input_value)
        elif input_value.name.startswith('y'):
            input_values[1].append(input_value)

    pattern = r'(...) (AND|OR|XOR) (...) -> (...)'
    gates: dict[str, (str, str, str)] = {}
    for gate in gate_connections:
        matches = re.fullmatch(pattern, gate)
        gates[matches[4]] = (matches[1], matches[3])
        value = Value(matches[4], op=matches[2])
        values[matches[4]] = value
        if value.name.startswith('z'):
            output_values.append(value)

    for value_name, (input_name_1, input_name_2) in gates.items():
        value = values[value_name]
        value.inputs.append(values[input_name_1])
        value.inputs.append(values[input_name_2])

    input_values[0].sort()
    input_values[1].sort()
    output_values.sort()

    return tuple(input_values), output_values


def topo_sort_recursive(value: Value, visited_values: set[str], sorted_values: list[Value]):
    if value.name not in visited_values:
        visited_values.add(value.name)
        for input_value in value.inputs:
            topo_sort_recursive(input_value, visited_values, sorted_values)
        sorted_values.append(value)


class Device:
    def __init__(self, x: list[Value], y: list[Value], z: list[Value]):
        self.x = x
        self.y = y
        self.z = z
        self.topo_sorted = []
        self.topo_sort()

    def topo_sort(self):
        visited_values = set()
        self.topo_sorted = []
        for value in self.z:
            topo_sort_recursive(value, visited_values, self.topo_sorted)

    def perform_calc(self):
        for value in self.topo_sorted:
            value.calc()

    def get_z(self) -> int:
        output_value = 0
        for n_bit in range(0, len(self.z)):
            output_value += self.z[n_bit].value * (1 << n_bit)
        return output_value

    def set_x(self, number_to_set: int):
        for n_bit in range(0, len(self.x)):
            self.x[n_bit].value = (number_to_set & (1 << n_bit)) >> n_bit

    def set_y(self, number_to_set: int):
        for n_bit in range(0, len(self.y)):
            self.y[n_bit].value = (number_to_set & (1 << n_bit)) >> n_bit

    def swap_values(self, a: Value, b: Value):
        temp = a.inputs
        a.inputs = b.inputs
        b.inputs = temp
        temp = a.op
        a.op = b.op
        b.op = temp
        self.topo_sort()

    def swap_by_names(self, a: str, b: str):
        self.swap_values(self.find_by_name(a), self.find_by_name(b))

    def find_by_name(self, name: str) -> Value:
        if name in self.x:
            return next(x for x in self.x if x.name == name)
        if name in self.x:
            return next(y for y in self.y if y.name == name)
        return next(a for a in self.topo_sorted if a.name == name)

    def check_add(self, x_value: int, y_value: int) -> bool:
        z_value = x_value + y_value
        self.set_x(x_value)
        self.set_y(y_value)
        try:
            self.perform_calc()
        except TypeError:
            return False
        return z_value == self.get_z()

    def is_bit_add_ok(self, bit: int) -> bool:
        return (self.check_add(1 << bit, 0)
                and self.check_add(0, 1 << bit)
                and (bit == 0 or self.check_add(1 << (bit - 1), 1 << (bit - 1)))
                and self.check_add(0, 0))

    def find_swaps(self, swaps_made: list[(Value, Value)] = None) -> list[(Value, Value)]:
        if swaps_made is None:
            swaps_made = []
        last_good_bit = -1
        do_not_swap = set()
        do_not_swap.update(self.x)
        do_not_swap.update(self.y)
        dependencies = []
        for bit in range(0, len(self.z)):
            if self.is_bit_add_ok(bit):
                try:
                    dep = self.z[bit].dependencies()
                    do_not_swap.update(dep)
                    dependencies.append(dep)
                except RecursionError:
                    break
                last_good_bit = bit
            else:
                break
        if last_good_bit == len(self.x) - 1:
            return swaps_made
        elif len(swaps_made) == 4:
            return []
        possible_swaps = []
        for i, a in enumerate(self.topo_sorted):
            if a in do_not_swap:
                continue
            for j in range(i + 1, len(self.topo_sorted)):
                b = self.topo_sorted[j]
                if b in do_not_swap:
                    continue
                valid = True
                for swap in swaps_made:
                    if a in swap or b in swap:
                        valid = False
                        break
                if valid:
                    self.swap_values(a, b)
                    good = True
                    if not self.is_bit_add_ok(last_good_bit + 1):
                        good = False
                    try:
                        dep = self.z[last_good_bit + 1].dependencies()
                    except RecursionError:
                        dep = set()
                    if last_good_bit > 1 and len(dep) - len(dependencies[last_good_bit]) != 6:
                        good = False
                    if good:
                        possible_swaps.append((a, b))
                    self.swap_values(a, b)
        for swap in possible_swaps:
            self.swap_values(*swap)
            swaps_attempted = copy(swaps_made)
            swaps_attempted.append(swap)
            swaps = self.find_swaps(swaps_attempted)
            self.swap_values(*swap)
            if swaps:
                return swaps


def solve_part1(file_name: str) -> int:
    (x, y), z = read_input(file_name)
    device = Device(x, y, z)
    device.perform_calc()
    return device.get_z()


def solve_part2(file_name: str) -> str:
    (x, y), z = read_input(file_name)
    device = Device(x, y, z)
    # device.swap_by_names('z09', 'nnf')
    # device.swap_by_names('z20','nhs' )
    # device.swap_by_names('kqh','ddn' )
    # device.swap_by_names('z34','wrc' )
    swaps = device.find_swaps()
    swaps = [value.name for swap in swaps for value in swap]
    swaps.sort()
    return ','.join(swaps)


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 48806532300520, 2: 'ddn,kqh,nhs,nnf,wrc,z09,z20,z34'}

assert_equal(solve_part1('test1.txt'), 2024, f'Incorrect answer to test')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
