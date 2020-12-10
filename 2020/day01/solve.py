import itertools
import functools
from typing import Optional, List


def find_sum(nums: List[int], n: int, target: int) -> Optional[List[int]]:
    for vals in itertools.combinations_with_replacement(nums, n):
        if sum(vals) == target:
            return vals
    return None


with open('input.txt', 'r') as f:
    nums = [int(i) for i in f.read().splitlines()]

TARGET = 2020
for n in [2, 3]:  # part 1 + 2
    res = find_sum(nums, n, TARGET)
    res_s = [str(i) for i in res]
    print(f'{" + ".join(res_s)} = {TARGET}\t\t{" * ".join(res_s)} = {functools.reduce(int.__mul__, res)}')
