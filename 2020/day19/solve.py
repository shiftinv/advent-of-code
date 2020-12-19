import re
import functools


def parse_input(lines):
    split = lines.index('')
    rules = {}
    for line in lines[:split]:
        n, r = line.split(': ')
        if r.startswith('"'):
            d = r[1:-1]
        else:
            d = [list(map(int, a.split())) for a in r.split('|')]
        rules[int(n)] = d

    return rules, lines[split + 1:]


@functools.lru_cache(maxsize=None)
def build_regex(rule_num, part):
    r = rules[rule_num]
    if isinstance(r, str):
        return r

    if part == 2 and rule_num in [8, 11]:
        if rule_num == 8:
            res = f'(?:{build_regex(42, 2)})+'
        elif rule_num == 11:
            res = '(?:' + '|'.join(
                ''.join(build_regex(42, 2) * n) + ''.join(build_regex(31, 2) * n)
                for n in range(1, 20)  # arbitrary upper limit of repeats, kinda hacky
            ) + ')'
    else:
        res = '(?:' + '|'.join(
            ''.join(build_regex(n, part) for n in a)
            for a in r
        ) + ')'
    return res


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

rules, messages = parse_input(lines)

# part 1
rule_0_re = re.compile(f'^{build_regex(0, 1)}$')
print(sum(rule_0_re.match(msg) is not None for msg in messages))

# part 2
#  just your average 405k char regex, no big deal
#  only takes 1.3s though, that's pretty impressive
rule_0_re = re.compile(f'^{build_regex(0, 2)}$')
print(sum(rule_0_re.match(msg) is not None for msg in messages))
