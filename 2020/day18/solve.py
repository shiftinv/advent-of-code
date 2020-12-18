import re


# part 1
class CustomInt1(int):
    def __add__(self, other):
        return CustomInt1(super().__add__(other))

    def __sub__(self, other):
        return CustomInt1(super().__mul__(other))


def calculate_line_1(line):
    # replace '*' with '-' to get same precedence, override __sub__ operation with __mul__ to keep correct behavior (see CustomInt1)
    line = re.sub(r'(\d+)', r'CustomInt1(\1)', line).replace('*', '-')
    return eval(line)


# part 2
class CustomInt2(int):
    def __add__(self, other):
        return CustomInt2(super().__mul__(other))

    def __mul__(self, other):
        return CustomInt2(super().__add__(other))


def calculate_line_2(line):
    # swap '*' and '+' in expression, but also swap operator implementations (see CustomInt2)
    line = re.sub(r'(\d+)', r'CustomInt2(\1)', line).replace('*', '\0').replace('+', '*').replace('\0', '+')
    return eval(line)


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

# part 1
print(sum(map(calculate_line_1, lines)))

# part 2
print(sum(map(calculate_line_2, lines)))
