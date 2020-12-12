def move_dir(x, y, d, n):
    if d == 'N':
        y += n
    elif d == 'E':
        x += n
    elif d == 'S':
        y -= n
    elif d == 'W':
        x -= n
    else:
        raise RuntimeError
    return x, y


def move(x, y, d, line):
    c = line[0]
    n = int(line[1:])

    if c in ['L', 'R']:
        d += (1 if c == 'L' else -1) * n
        d %= 360
    else:
        if c == 'F':
            c = 'ENWS'[d // 90]
        x, y = move_dir(x, y, c, n)

    return x, y, d


def rotate(wx, wy, pd, d):
    # don't really want to look up the proper maths behind rotating a point around another point
    f = -1 if pd < d else 1
    for _ in range(abs(d - pd) // 90):
        nx = f * wy
        ny = -f * wx
        wx, wy = nx, ny
    return wx, wy


def move_with_waypoint(x, y, wx, wy, d, line):
    c = line[0]
    n = int(line[1:])

    if c in ['L', 'R']:
        prev_d = d
        d += (1 if c == 'L' else -1) * n
        d %= 360
        wx, wy = rotate(wx, wy, prev_d, d)
    else:
        if c == 'F':
            c = 'ENWS'[d // 90]
            x += wx * n
            y += wy * n
        else:
            wx, wy = move_dir(wx, wy, c, n)

    return x, y, wx, wy, d


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

# part 1
p1 = (0, 0, 0)
for line in lines:
    p1 = move(*p1, line)
print(abs(p1[0]) + abs(p1[1]))

# part 2
p2 = (0, 0, 10, 1, 0)
for line in lines:
    p2 = move_with_waypoint(*p2, line)
print(abs(p2[0]) + abs(p2[1]))
