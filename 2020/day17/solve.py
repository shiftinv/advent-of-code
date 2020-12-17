import itertools
import functools
from collections import defaultdict


def init_space(lines, dim):
    d = defaultdict(lambda: False)
    pad = [0] * (dim - 2)
    for x in range(len(lines)):
        for y in range(len(lines[x])):
            pos = (x, y, *pad)
            d[pos] = (lines[x][y] == '#')
    return d


@functools.lru_cache(maxsize=None)
def get_neighbors(pos):
    return [
        tuple(c + dc for c, dc in zip(pos, dpos))
        for dpos in itertools.product(range(-1, 2), repeat=len(pos))
        if any(c != 0 for c in dpos)
    ]


def cycle(space):
    checked = set()
    new_space = defaultdict(lambda: False)
    for pos in [k for k, v in space.items() if v]:
        neighbors = get_neighbors(pos)
        num_active_neighbors = sum(space[n] for n in neighbors)
        # rule 1
        new_space[pos] = (num_active_neighbors in [2, 3])
        # rule 2
        for inactive_neighbor in (n for n in neighbors if n not in checked and not space[n]):
            checked.add(inactive_neighbor)
            num_active_neighbors2 = sum(space[n] for n in get_neighbors(inactive_neighbor))
            new_space[inactive_neighbor] = (num_active_neighbors2 == 3)
    return new_space


def simulate(space, n):
    for i in range(n):
        print(f'cycle {i + 1}/{n}')
        space = cycle(space)
    return space


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()


# part 1
start_space = init_space(lines, 3)
space = simulate(start_space, 6)
print(sum(1 for k, v in space.items() if v))

# part 2
start_space = init_space(lines, 4)
space = simulate(start_space, 6)
print(sum(1 for k, v in space.items() if v))
