def nth_spoken_number(n):
    last_spoken = {}
    prev_num = -1
    prev_first_time = False
    for i in range(n):
        if i < len(numbers):
            num = numbers[i]
        else:
            if prev_first_time:
                num = 0
            else:
                num = i - 1 - last_spoken[prev_num]
        prev_first_time = num not in last_spoken
        last_spoken[prev_num] = i - 1
        prev_num = num
    return prev_num


with open('input.txt', 'r') as f:
    numbers = list(map(int, f.read().split(',')))

# part 1
print(nth_spoken_number(2020))

# part 2
print(nth_spoken_number(30000000))
