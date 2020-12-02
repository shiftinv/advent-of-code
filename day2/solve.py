import re


def parse_line(line):
    m = re.match(r'^(\d+)-(\d+) (\w): (\w+)$', line)
    return int(m[1]), int(m[2]), m[3], m[4]


def check_valid_1(tup):
    return tup[3].count(tup[2]) in range(tup[0], tup[1] + 1)


def check_valid_2(tup):
    chars = [tup[3][tup[0] - 1], tup[3][tup[1] - 1]]
    return tup[2] in chars and chars[0] != chars[1]


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

parsed = [parse_line(line) for line in lines]
# part 1
print(len(list(filter(check_valid_1, parsed))))
# part 2
print(len(list(filter(check_valid_2, parsed))))
