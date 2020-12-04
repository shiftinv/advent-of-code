import re


def is_valid_1(passport):
    return {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} <= passport.keys()


def is_valid_2(passport):
    # matching number ranges with regex, because why not
    return \
        1920 <= int(passport['byr']) <= 2002 and \
        2010 <= int(passport['iyr']) <= 2020 and \
        2020 <= int(passport['eyr']) <= 2030 and \
        re.match(r'^(1([5-8][0-9]|9[0-3])cm|(59|6[0-9]|7[0-6])in)$', passport['hgt']) and \
        re.match(r'^#[0-9a-f]{6}$', passport['hcl']) and \
        passport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'} and \
        re.match(r'^[0-9]{9}$', passport['pid'])


with open('input.txt', 'r') as f:
    passports_strs = f.read().split('\n\n')
passports = [
    {a: b for kv in s.split() for a, b in [kv.split(':')]}
    for s in passports_strs
]

# part 1
valid_p1 = list(filter(is_valid_1, passports))
print(len(valid_p1))

# part 2
valid_p2 = list(filter(is_valid_2, valid_p1))
print(len(valid_p2))
