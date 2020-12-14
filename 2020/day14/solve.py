import re


def parse_line(line):
    if line.startswith('mask'):
        return line.split(' ')[2]
    else:
        m = re.match(r'^mem\[(\d+)\] = (\d+)$', line)
        return int(m[1]), int(m[2])


def set_bit(value, shift, bit):
    if bit == 1:
        return value | (1 << shift)
    else:
        return value & ~(1 << shift)


# part 1
def apply_mask_1(value, mask):
    for i, b in enumerate(mask[::-1]):
        if b.isdigit():
            value = set_bit(value, i, int(b))
    return value


def run_program_1(lines):
    memory = {}
    curr_mask = None  # first line will always be a bitmask
    for line in lines:
        parsed = parse_line(line)
        if isinstance(parsed, tuple):
            memory[parsed[0]] = apply_mask_1(parsed[1], curr_mask)
        else:
            curr_mask = parsed
    return memory


# part 2
def apply_mask_2(value, mask):
    ones = []
    floating = []
    for i, b in enumerate(mask[::-1]):
        if b == 'X':
            floating.append(i)
        elif b == '1':
            ones.append(i)

    for i in ones:
        value |= (1 << i)
    written_addresses = []
    # iterate through possible configurations of floating bits
    # this is slow, but it works™ (BMI2 PDEP would be useful, but this isn't C/C++)
    for b in range(2 ** len(floating)):
        new_value = value
        for i, float_index in enumerate(floating):
            new_value = set_bit(new_value, float_index, (b >> i) & 1)
        written_addresses.append(new_value)
    return written_addresses


def run_program_2(lines):
    memory = {}
    curr_mask = None  # first line will always be a bitmask
    for line in lines:
        parsed = parse_line(line)
        if isinstance(parsed, tuple):
            addresses = apply_mask_2(parsed[0], curr_mask)
            for addr in addresses:
                memory[addr] = parsed[1]
        else:
            curr_mask = parsed
    return memory


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

# part 1
print(sum(run_program_1(lines).values()))

# part 2
print(sum(run_program_2(lines).values()))
