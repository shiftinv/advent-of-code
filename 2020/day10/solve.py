import functools


def find_diffs():
    diffs = []
    prev = 0
    for n in nums:
        diffs.append(n - prev)
        prev = n
    diffs.append(3)
    return diffs


@functools.lru_cache(maxsize=None)
def num_paths_to(idx):
    n = nums[idx]
    paths = 1 if n <= 3 else 0  # num can be reached from start if <= 3

    for other_idx in range(max(0, idx - 3), idx):  # check up to 3 numbers before
        if n - nums[other_idx] > 3:  # maximum allowed difference between adapters is 3
            continue
        paths += num_paths_to(other_idx)

    return paths


with open('input.txt', 'r') as f:
    nums = sorted(list(map(int, f.read().splitlines())))

# part 1
diffs = find_diffs()
print(diffs.count(1) * diffs.count(3))

# part 2
print(num_paths_to(len(nums) - 1))
