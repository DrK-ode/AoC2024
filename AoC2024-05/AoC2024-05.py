import time

from numpy.testing import assert_equal


def read_input(input_file: str) -> (dict[int, list[int]], list[int]):
    with open(input_file, 'r') as file:
        rules, books = file.read().split('\n\n')
        rules = [[int(page) for page in rule.split('|')] for rule in rules.splitlines()]
        books = [[int(page) for page in page_list.split(',')] for page_list in books.splitlines()]
        rule_dict = {}
        for before, after in rules:
            if before not in rule_dict:
                rule_dict[before] = [after]
            else:
                rule_dict[before].append(after)
        return rule_dict, books


def check_page_list(page_list: list[int], rules: dict[int, list[int]]) -> (bool, int):
    for index, page in enumerate(page_list):
        if page not in rules:
            continue
        for later_page in rules[page]:
            if later_page in page_list[:index]:
                return False, fixed_middle_page(page_list, rules)
    return True, page_list[len(page_list) // 2]


# Recursively adds all later pages before adding the page itself
def insert_page(reversed_page_list: list[int], original_page_list: list[int], rules: dict[int, list[int]], page: int):
    if page in reversed_page_list:
        return
    pages_after = rules.get(page)
    if pages_after is not None:
        for page_after in pages_after:
            if page_after in original_page_list:
                insert_page(reversed_page_list, original_page_list, rules, page_after)
    reversed_page_list.append(page)


def fixed_middle_page(page_list: list[int], rules: dict[int, list[int]]) -> int:
    # Because it is easier to append and the middle page will still be the same
    reversed_fixed_page_list = []
    for page_number in page_list:
        insert_page(reversed_fixed_page_list, page_list, rules, page_number)
    return reversed_fixed_page_list[len(reversed_fixed_page_list) // 2]


def solve_part1and2(input_file: str) -> (int, int):
    rules, page_lists = read_input(input_file)
    correct_middle_page_sum = 0
    fixed_middle_page_sum = 0
    for page_list in page_lists:
        correctly_ordered, middle_page = check_page_list(page_list, rules)
        if correctly_ordered:
            correct_middle_page_sum += middle_page
        else:
            fixed_middle_page_sum += middle_page
    return correct_middle_page_sum, fixed_middle_page_sum


def solve_parts() -> (int, int):
    duration = time.perf_counter()
    answer = solve_part1and2('input.txt')
    duration = time.perf_counter() - duration
    print(f'Answer to part 1: {answer[0]}\nanswer to part 2: {answer[1]}\nfound in {duration:.2e} seconds')
    return answer


correct_answers = (4689, 6336)
assert_equal(solve_part1and2('test1.txt'), (143, 123), 'Incorrect answer to example.')
assert_equal(solve_part1and2('input.txt'), correct_answers, f'Incorrect answer to part 1')

solve_parts()
