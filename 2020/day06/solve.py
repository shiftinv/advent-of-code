with open('input.txt', 'r') as f:
    data = f.read()

groups = [g.splitlines() for g in data.split('\n\n')]
groups_sets = [[set(p) for p in g] for g in groups]

# part 1
print(sum(
    len(set.union(*g)) for g in groups_sets
))

# part 2
print(sum(
    len(set.intersection(*g)) for g in groups_sets
))
