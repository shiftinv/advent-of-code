import re
import functools


def parse_line(line):
    outer_color, *inner_bags = re.findall(r'(?:(\d+) )?(\w+ \w+) bag', line)
    outer_color = outer_color[1]
    inner_bags = {c: int(n) for n, c in inner_bags if c != 'no other'}
    return outer_color, inner_bags


# part 1
def get_containers(color):
    return [
        outer_color for outer_color, inner in parsed_input.items()
        if color in inner.keys()
    ]


def find_all_containers(color):
    containers = set()
    queue = [color]
    while queue:
        col = queue.pop(0)

        cont = get_containers(col)
        new_containers = set(cont) - containers

        containers.update(new_containers)
        queue.extend(new_containers)

    return containers


# part 2
@functools.lru_cache(maxsize=2020)
def count_contents(color):
    inner = parsed_input[color]
    return sum(
        count * (1 + count_contents(inner_col))
        for inner_col, count in inner.items()
    )


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

parsed_input = dict(map(parse_line, lines))

# part 1
print(len(find_all_containers('shiny gold')))

# part 2
print(count_contents('shiny gold'))
