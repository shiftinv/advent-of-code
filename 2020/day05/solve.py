def binary_partition(slices, lower_char, start, end):
    for s in slices:
        mid = start + (end - start) // 2
        if s == lower_char:
            end = mid
        else:
            start = mid
    assert end - 1 == start
    return start


def get_id(bp):
    row = binary_partition(bp[:7], 'F', 0, 128)
    col = binary_partition(bp[7:], 'L', 0, 8)
    return row * 8 + col


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

# part 1
ids = list(map(get_id, lines))
print(max(ids))

# part 2
missing = set(range(0, 128 * 8)) - set(ids)
print(next(filter(lambda i: i - 1 in ids and i + 1 in ids, missing)))
