from typing import Dict, List, Tuple


def parse_input(data: str) -> Dict[int, Tuple[str]]:
    tiles = {}
    for block in data.split('\n\n'):
        if not block:
            continue
        lines = block.splitlines()
        id = int(lines[0].split(' ')[1][:-1])
        tiles[id] = tuple(lines[1:])
    return tiles


def get_borders(tile: List[str]) -> List[str]:
    transposed = list(zip(*tile))
    return [tile[0], ''.join(transposed[-1]), tile[-1][::-1], ''.join(transposed[0])[::-1]]  # NESW clockwise


def rotate(tile, times):
    for _ in range(times):
        tile = tuple(''.join(r) for r in zip(*tile[::-1]))
    return tile


def flip(tile, vertical):
    if vertical:
        return tuple(r[::-1] for r in tile)
    else:
        return tile[::-1]


def align_borders(target, target_dir, new_tile_data, new_tile_borders):
    new_dir = (target_dir + 2) % 4
    if target in new_tile_borders:
        # need to flip
        index = new_tile_borders.index(target)
        flipped_tile = flip(new_tile_data, index % 2 == 0)
        return rotate(flipped_tile, (new_dir - index) % 4)
    elif target[::-1] in new_tile_borders:
        # no flip
        index = new_tile_borders.index(target[::-1])
        return rotate(new_tile_data, (new_dir - index) % 4)
    else:
        return None


def is_free_border(tile_map, pos, direction):
    if direction == 0 and tile_map[pos[1] - 1][pos[0]] is not None:
        return False
    if direction == 1 and tile_map[pos[1]][pos[0] + 1] is not None:
        return False
    if direction == 2 and tile_map[pos[1] + 1][pos[0]] is not None:
        return False
    if direction == 3 and tile_map[pos[1]][pos[0] - 1] is not None:
        return False
    return True


def shrink_map(tile_map):
    used_tiles = [(x, y) for y, row in enumerate(tile_map) for x, tile in enumerate(row) if tile]
    min_pos = min(used_tiles)
    max_pos = max(used_tiles)
    return [row[min_pos[0]:max_pos[0] + 1] for row in tile_map[min_pos[1]:max_pos[1] + 1]]


class NestedBreak(Exception):
    pass


def reassemble(tiles):
    # maximum required space
    tile_map = [[None] * (len(tiles) * 2) for _ in range(len(tiles) * 2)]
    first_tile, *unused_tiles = tiles.items()

    tile_map[len(tiles)][len(tiles)] = first_tile
    map_borders = {(len(tiles), len(tiles)): get_borders(first_tile[1])}  # initial tile at center
    unused_tiles = {tile_id: get_borders(tile) for tile_id, tile in unused_tiles}

    # this is terrible code - it's a pain to debug this, but it works™
    while unused_tiles:
        try:
            for new_tile_id, new_tile_borders in unused_tiles.items():
                new_tile_data = tiles[new_tile_id]
                for tile_pos, tile_borders in map_borders.items():
                    for i, free_border in enumerate(tile_borders):
                        if not is_free_border(tile_map, tile_pos, i):
                            continue
                        aligned_tile = align_borders(free_border, i, new_tile_data, new_tile_borders)
                        if not aligned_tile:
                            continue
                        new_pos = (tile_pos[0] + (i % 2 == 1) * (2 - i), tile_pos[1] + (i % 2 == 0) * (i - 1))
                        # add new tile to tile map
                        tile_map[new_pos[1]][new_pos[0]] = (new_tile_id, aligned_tile)

                        # add borders of new tile
                        map_borders[new_pos] = get_borders(aligned_tile)
                        # remove new tile from unused tiles
                        unused_tiles.pop(new_tile_id)

                        raise NestedBreak  # python y u no `break <label>`
        except NestedBreak:
            pass

    return shrink_map(tile_map)


def compare_pattern(char_map, x, y, pattern):
    for yc, row in enumerate(pattern):
        for xc, compare_char in enumerate(row):
            if compare_char != ' ' and char_map[y + yc][x + xc] != compare_char:
                return False
    return True


def count_sea_monster_fields(char_map):
    pattern = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    ]
    found = 0
    for y in range(len(char_map) - len(pattern)):
        for x in range(len(char_map[y]) - len(pattern[0])):
            if compare_pattern(char_map, x, y, pattern):
                found += 1
    return found * sum(r.count('#') for r in pattern)


with open('input.txt', 'r') as f:
    data = f.read()

tiles = parse_input(data)

# part 1
new_map = reassemble(tiles)
print(new_map[0][0][0] * new_map[0][-1][0] * new_map[-1][0][0] * new_map[-1][-1][0])

# part 2
new_map_tiles = [[tile[1] for tile in row] for row in new_map]
joined_map = [
    ''.join(char_row)
    for tile_row in new_map_tiles
    for char_row in zip(*[[r[1:-1] for r in tile[1:-1]] for tile in tile_row])
]
sea_monster_fields = None
for i in range(8):  # try all orientations
    if i == 4:
        joined_map = flip(joined_map, True)
    sea_monster_fields = count_sea_monster_fields(joined_map)
    if sea_monster_fields:
        break
    joined_map = rotate(joined_map, 1)
print(sum(row.count('#') for row in joined_map) - sea_monster_fields)
