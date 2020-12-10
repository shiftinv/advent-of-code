import itertools


def check_sum(offset):
    assert offset >= 25
    return any(a + b == numbers[offset] for a, b in itertools.combinations(numbers[offset - 25:offset], 2))


def find_contiguous_set(target):
    for start in range(len(numbers)):
        s = numbers[start]
        for end in range(start + 1, len(numbers)):
            s += numbers[end]
            if s == target:
                r = numbers[start:end + 1]
                return min(r), max(r)
            elif s > target:
                break


with open('input.txt', 'r') as f:
    numbers = list(map(int, f.read().splitlines()))

# part 1
invalid_num = next(numbers[offset] for offset in range(25, len(numbers)) if not check_sum(offset))
print(invalid_num)

# part 2
print(sum(find_contiguous_set(invalid_num)))
