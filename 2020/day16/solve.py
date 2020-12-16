import re
import functools
from typing import Tuple, Dict, List, Set


def parse_input(data: str) -> Tuple[Dict[str, List[int]], List[int], List[List[int]]]:
    blocks = data.split('\n\n', 1)

    rules = {r[0]: tuple(map(int, r[1:])) for r in re.findall(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', blocks[0])}
    tickets = []
    for line in blocks[1].splitlines():
        t = list(map(int, re.findall(r'(\d+)', line)))
        if t:
            tickets.append(t)
    my_ticket, *nearby_tickets = tickets

    return rules, my_ticket, nearby_tickets


def in_range(value: int, rule_ranges: List[int]) -> bool:
    return rule_ranges[0] <= value <= rule_ranges[1] or rule_ranges[2] <= value <= rule_ranges[3]


def find_invalid(rules: List[List[int]], ticket: List[int]) -> List[int]:
    invalid = []
    for value in ticket:
        for rule in rules:
            if in_range(value, rule):
                break
        else:
            invalid.append(value)
    return invalid


def filter_indices(fields: Dict[Tuple[str, List[int]], Set[int]], ticket: List[int]) -> None:
    for rule, possible_indices in fields.items():
        for index in possible_indices.copy():
            if not in_range(ticket[index], rule[1]):
                possible_indices.remove(index)


def match_fields(fields: Dict[Tuple[str, List[int]], Set[int]]) -> None:
    while True:
        # find field with only one possible ticket value index
        only_option = next((p for p in fields.items() if isinstance(p[1], set) and len(p[1]) == 1), None)
        if only_option is None:
            # done
            assert all(isinstance(s, int) for s in fields.values())
            return
        index = tuple(only_option[1])[0]
        fields[only_option[0]] = index
        # remove index from all other fields
        for s in fields.values():
            if isinstance(s, set):
                s.remove(index)


with open('input.txt', 'r') as f:
    data = f.read()

rules, my_ticket, nearby_tickets = parse_input(data)

# filter valid/invalid tickets
valid_tickets = []
invalid_values = []
for ticket in nearby_tickets:
    invalid = find_invalid(rules.values(), ticket)
    if invalid:
        invalid_values.extend(invalid)
    else:
        valid_tickets.append(ticket)

# part 1
print(sum(invalid_values))

# part 2
fields = {p: set(range(len(rules))) for p in rules.items()}
for ticket in valid_tickets:
    filter_indices(fields, ticket)
match_fields(fields)
print(functools.reduce(int.__mul__, (my_ticket[i] for r, i in fields.items() if r[0].startswith('departure'))))
