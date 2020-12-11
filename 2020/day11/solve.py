def get_adjacent(curr_data, x, y):
    return [
        curr_data[y2][x2]
        for y2 in range(y - 1, y + 2)
        for x2 in range(x - 1, x + 2)
        if (x2, y2) != (x, y)
        and 0 <= y2 < len(curr_data)
        and 0 <= x2 < len(curr_data[0])
    ]


def get_adjacent_line(curr_data, x, y):
    adj = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dx, dy) == (0, 0):
                continue

            x2 = x
            y2 = y
            while True:
                x2 += dx
                y2 += dy
                if not (0 <= y2 < len(curr_data)) or not (0 <= x2 < len(curr_data[0])):
                    break  # reached end of map
                if curr_data[y2][x2] != '.':
                    adj.append(curr_data[y2][x2])  # found seat
                    break
    return adj


def update(curr_data, func, empty_thresh):
    new_data = [line[:] for line in curr_data]  # copy
    changed = False
    for y in range(len(curr_data)):
        for x in range(len(curr_data[0])):
            t = curr_data[y][x]
            if t == 'L' and func(curr_data, x, y).count('#') == 0:
                new_data[y][x] = '#'
                changed = True
            elif t == '#' and func(curr_data, x, y).count('#') >= empty_thresh:
                new_data[y][x] = 'L'
                changed = True
    return new_data, changed


def simulate(data, func, empty_thresh):
    i = 1
    while True:
        # print(f'update {i}')
        i += 1
        new_data, changed = update(data, func, empty_thresh)
        if not changed:
            break
        data = new_data
    return new_data


with open('input.txt', 'r') as f:
    data = [list(line) for line in f.read().splitlines()]

# part 1
new_data = simulate(data, get_adjacent, 4)
print(sum(line.count('#') for line in new_data))

# part 2
new_data = simulate(data, get_adjacent_line, 5)
print(sum(line.count('#') for line in new_data))
