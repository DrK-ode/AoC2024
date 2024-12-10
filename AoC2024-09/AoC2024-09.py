import string
import time

from numpy.testing import assert_equal


def read_input(input_file: str) -> list[int]:
    with open(input_file, 'r') as file:
        return [int(digit) for digit in file.read().rstrip()]


class DiskIterator:
    def __init__(self, diskmap: list[int], is_front: bool):
        self._diskmap = diskmap
        self._diskmap_index = 0 if is_front else len(diskmap) - 1
        self._block_index = 0
        self._direction = 1 if is_front else -1
        self._buffer_size = diskmap[self._diskmap_index]

    def __lt__(self, other):
        return self._diskmap_index < other.diskmap_index()

    def __gt__(self, other):
        return self._diskmap_index > other.diskmap_index()

    def __eq__(self, other):
        return self._diskmap_index == other.diskmap_index()

    def buffer(self) -> int:
        return self._buffer_size

    def buffer_empty(self) -> bool:
        return self._buffer_size == 0

    def block_index(self) -> int:
        return self._block_index

    def diskmap_index(self) -> int:
        return self._diskmap_index

    def is_file(self) -> bool:
        return self._diskmap_index % 2 == 0

    def file_id(self) -> int:
        return self._diskmap_index // 2

    def next(self):
        self._diskmap_index += self._direction
        self.update()

    def update(self):
        if 0 <= self._diskmap_index < len(self._diskmap):
            self._block_index += self._direction * self._buffer_size
            self._buffer_size = self._diskmap[self._diskmap_index]
        else:
            self._block_index = None
            self._buffer_size = None

    def next_file(self):
        self.next()
        if not self.is_file():
            self.next()

    def next_free_space(self):
        self.next()
        if self.is_file():
            self.next()

    def process_blocks(self, amount=None) -> int:
        if amount is None or amount > self._buffer_size:
            amount = self._buffer_size
        self._buffer_size -= amount
        self._block_index += amount
        return amount


def solve_part1(input_file: str) -> int:
    diskmap = read_input(input_file)
    total_checksum = 0
    front_iter = DiskIterator(diskmap, True)
    back_iter = DiskIterator(diskmap, False)
    while front_iter < back_iter:
        if front_iter.is_file():
            blocks = front_iter.process_blocks()
            checksum = front_iter.file_id() * (blocks * front_iter.block_index() - blocks * (blocks + 1) // 2)
            total_checksum += checksum
            front_iter.next()
        else:
            blocks = back_iter.process_blocks(front_iter.buffer())
            blocks = front_iter.process_blocks(blocks)
            checksum = back_iter.file_id() * (blocks * front_iter.block_index() - blocks * (blocks + 1) // 2)
            total_checksum += checksum
            if front_iter.buffer_empty():
                front_iter.next()
            if back_iter.buffer_empty():
                back_iter.next_file()
    if front_iter == back_iter:
        blocks = back_iter.process_blocks()
        total_checksum += front_iter.file_id() * front_iter.block_index() - blocks + 1

    return total_checksum


def find_free_space(diskmap: list[int], size: int) -> int:
    free_iter = DiskIterator(diskmap, True)
    free_iter.next_free_space()
    while free_iter.diskmap_index() < len(diskmap) and free_iter.buffer() < size:
        free_iter.next_free_space()
    return free_iter.diskmap_index()


def disk_checksum(diskmap: list[int], file_ids: list[int]):
    front_iter = DiskIterator(diskmap, True)
    total_checksum = 0
    while front_iter.diskmap_index() < len(diskmap):
        blocks = front_iter.process_blocks()
        checksum = file_ids[front_iter.diskmap_index() // 2] * (
                blocks * front_iter.block_index() - blocks * (blocks + 1) // 2)
        total_checksum += checksum
        front_iter.next_file()
    return total_checksum


def solve_part2(input_file: str) -> int:
    diskmap = read_input(input_file)
    # files[i] = [data_start, data-length]
    files = [[0, 0] for i in range(0, len(diskmap) // 2 + 1)]
    spaces = [[0, 0] for i in range(0, len(diskmap) // 2)]
    block_count = 0
    for i, size in enumerate(diskmap):
        if i % 2 == 0:
            files[i // 2][0] = block_count
            files[i // 2][1] = size
        else:
            spaces[i // 2][0] = block_count
            spaces[i // 2][1] = size
        block_count += size
    for file in reversed(files):
        for space_index, space in enumerate(spaces):
            if space[0] >= file[0]:
                break
            if space[1] >= file[1]:
                file[0] = space[0]
                space[0] += file[1]
                space[1] -= file[1]
                break
    checksum = 0
    for file_id, [file_start, file_size] in enumerate(files):
        checksum += file_id * (file_size * file_start + file_size * (file_size - 1) // 2)
    return checksum


def solve_part(part: int) -> int:
    if not 0 < part <= 2:
        raise Exception("Part must be either 1 or 2.")
    duration = time.perf_counter()
    answer = solve_part1('input.txt') if part == 1 else solve_part2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part {part}: {answer}, found in {duration:.2e} seconds')
    return answer


correct_answers = {1: 6356833654075, 2: 6389911791746}

assert_equal(solve_part1('test1.txt'), 1928, 'Incorrect answer to example.')
assert_equal(solve_part1('input.txt'), correct_answers[1], f'Incorrect answer to part 1')
assert_equal(solve_part2('test1.txt'), 2858, 'Incorrect answer to example.')
assert_equal(solve_part2('input.txt'), correct_answers[2], f'Incorrect answer to part 2')

for p in [1, 2]:
    solve_part(p)
