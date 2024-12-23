import time

from numpy.testing import assert_equal


def read_input(input_file: str) -> dict[str, set[str]]:
    node_connections = {}
    for a, b in [line.rstrip().split('-') for line in open(input_file, 'r').readlines()]:
        node_connections.setdefault(a, set())
        node_connections.setdefault(b, set())
        node_connections[a].add(b)
        node_connections[b].add(a)
    return node_connections


def grow_groups(network_connections: dict[str, set[str]], groups: dict[tuple[str, ...], set[str]],
                max_generations: int = -1) -> list[tuple[str, ...]]:
    if max_generations == 0:
        return list(groups.keys())
    groups_in_next_generation = {}
    for members, common_connections in groups.items():
        for candidate in common_connections:
            new_members = tuple(sorted([*members, candidate]))
            if new_members in groups_in_next_generation:
                continue
            groups_in_next_generation[new_members] = common_connections & network_connections[candidate]
    if not groups_in_next_generation:
        return list(groups.keys())
    else:
        return grow_groups(network_connections, groups_in_next_generation, max_generations - 1)


def find_network_groups(file_name: str, group_size: int) -> list[tuple[str, ...]]:
    network_connections = read_input(file_name)
    start_groups = {}
    for node, connections in network_connections.items():
        start_groups[(node,)] = connections
    return grow_groups(network_connections, start_groups, group_size - 1)


def solve_part1(file_name: str) -> int:
    tri_groups = find_network_groups(file_name, 3)
    number_of_clusters = 0
    for node_i, node_j, node_k in tri_groups:
        if node_i[0] == 't' or node_j[0] == 't' or node_k[0] == 't':
            number_of_clusters += 1
    return number_of_clusters


def solve_part2(file_name: str) -> str:
    largest_groups = find_network_groups(file_name, -1)
    assert_equal(len(largest_groups), 1)
    return ','.join(largest_groups[0])


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 1352, 2: 'dm,do,fr,gf,gh,gy,iq,jb,kt,on,rg,xf,ze'}

assert_equal(solve_part1('test1.txt'), 7, f'Incorrect answer to test')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test1.txt'), 'co,de,ka,ta', f'Incorrect answer to test')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
