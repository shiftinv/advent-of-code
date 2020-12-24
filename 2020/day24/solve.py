import collections
import functools


def parse_input(lines):
    tiles = []
    for line in lines:
        steps = []
        for char in line:
            if steps and steps[-1] in ['n', 's']:
                steps[-1] += char
            else:
                steps.append(char)
        tiles.append(tuple(steps))
    return tiles


@functools.lru_cache(maxsize=None)
def get_pos(steps, start_x=0, start_y=0):
    x = start_x
    y = start_y
    for step in steps:
        if step == 'e':
            x += 1
        elif step == 'w':
            x -= 1
        else:
            if step[1] == 'e':
                x += y % 2
            else:
                x -= 1 - y % 2
            if step[0] == 'n':
                y += 1
            else:
                y -= 1
    return x, y


@functools.lru_cache(maxsize=None)
def get_neighbors(x, y):
    return [get_pos((step,), x, y) for step in ['ne', 'e', 'se', 'sw', 'w', 'nw']]


@functools.lru_cache(maxsize=None)
def step_day(black_tiles):
    new_black_tiles = []
    seen = set()
    for tile in black_tiles:
        neighbors = get_neighbors(*tile)
        if sum(1 for n in neighbors if n in black_tiles) in [1, 2]:
            # not flipped to white, keep tile
            new_black_tiles.append(tile)
        for neighbor in neighbors:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            if neighbor in black_tiles:
                continue  # only consider white tiles
            neighbors2 = get_neighbors(*neighbor)
            if sum(1 for n in neighbors2 if n in black_tiles) == 2:
                # flip white tile to black
                new_black_tiles.append(neighbor)
    return tuple(new_black_tiles)


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

tiles = parse_input(lines)
positions = list(map(get_pos, tiles))

# part 1
counter = collections.Counter(positions)
start_black_tiles = tuple(p for p, c in counter.items() if c % 2 == 1)
print(len(start_black_tiles))

# part 2
curr_black_tiles = start_black_tiles
for _ in range(100):
    curr_black_tiles = step_day(curr_black_tiles)
print(len(curr_black_tiles))
