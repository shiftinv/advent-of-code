def step(offset: int, acc: int):
    opcode, arg = program[offset]
    # print(f'{offset:04d}: {opcode} {arg}')

    if opcode == 'jmp':
        offset += arg
    else:
        if opcode == 'acc':
            acc += arg
        offset += 1
    return offset, acc


def emulate():
    seen = set()
    curr_offset = 0
    curr_acc = 0
    while curr_offset not in seen and curr_offset != len(lines):
        seen.add(curr_offset)
        curr_offset, curr_acc = step(curr_offset, curr_acc)
    return curr_offset, curr_acc


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()
program = [(o, int(a)) for line in lines for o, a in [line.split()]]

# part 1
_, curr_acc = emulate()
print(curr_acc)

# part 2
for i in range(len(program)):
    orig_opcode, orig_arg = program[i]
    if orig_opcode in ['jmp', 'nop']:
        # swap jmp/nop
        program[i] = ('jmp' if orig_opcode == 'nop' else 'nop', orig_arg)

        # emulate, check if program terminated
        offset, acc = emulate()
        if offset == len(program):
            print(acc)
            break

        # restore original instruction
        program[i] = (orig_opcode, orig_arg)
