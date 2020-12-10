import functools
from typing import List


def count_trees(map: List[str], x_delta: int, y_delta: int) -> int:
    trees = 0
    for y in range(0, len(map), y_delta):
        x = y // y_delta * x_delta
        if map[y][x % len(map[0])] == '#':
            trees += 1
    return trees


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

# part 1
print(count_trees(lines, 3, 1))

# part 2
print(functools.reduce(
    int.__mul__,
    (count_trees(lines, x_d, y_d) for x_d, y_d in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)))
))
