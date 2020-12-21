import re
import collections


def parse_input(lines):
    lists = []
    for line in lines:
        split = re.sub(r'[(),]', '', line).split(' ')
        mid = split.index('contains')
        lists.append((split[:mid], split[mid + 1:]))
    return lists


def find_matching_ingredients(allergen, found):
    lists = [k for k, v in data if allergen in v]
    all_ingredients = [i for l in lists for i in l]
    counter = collections.Counter(all_ingredients)
    # collect ingredients that are present in all lists (assuming no duplicates per list) and haven't been assigned yet
    return [k for k, v in counter.items() if v == len(lists) and k not in found]


def find_allergen_ingredients():
    allergens_left = set(a for t in data for a in t[1])
    found_map = {}  # maps ingredients to contained allergens
    while allergens_left:
        for allergen in allergens_left:
            matching = find_matching_ingredients(allergen, found_map)
            if len(matching) == 1:
                allergens_left.remove(allergen)
                found_map[matching[0]] = allergen
                break
        else:
            # no break in loop, something went wrong
            raise RuntimeError
    return found_map


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

data = parse_input(lines)

# part 1
allergen_map = find_allergen_ingredients()
print(len([i for t in data for i in t[0] if i not in allergen_map]))

# part 2
print(','.join(sorted(allergen_map.keys(), key=lambda k: allergen_map[k])))
