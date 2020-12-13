import math


def next_departure(min_time, interval):
    return math.ceil(min_time / interval) * interval


def check_valid_schedule(schedule, start_time):
    for bus_id, bus_offset in schedule:
        if (start_time + bus_offset) % bus_id != 0:
            return False
    return True


with open('input.txt', 'r') as f:
    lines = f.read().splitlines()

min_timestamp = int(lines[0])
schedule = lines[1].split(',')
assert schedule[0] != 'x'  # things will break if the first schedule entry is not a bus ID

# part 1
bus_ids = [int(i) for i in schedule if i != 'x']
next_departures = {i: next_departure(min_timestamp, i) for i in bus_ids}
next_bus = min(next_departures.items(), key=lambda kv: kv[1])
print(next_bus[0] * (next_bus[1] - min_timestamp))


# part 2
schedule_with_offset = [(int(bus_id), i) for i, bus_id in enumerate(schedule) if bus_id != 'x']

min_start = 0
solution_step = bus_ids[0]
for schedule_offset, (bus_id, bus_offset) in enumerate(schedule_with_offset):
    # find valid solution for first 0..i buses based on solutions for first 0..i-1 buses
    start = min_start
    while True:
        # check if schedule is valid up to this bus at the current timestep
        if (check_valid_schedule(schedule_with_offset[:schedule_offset + 1], start)):
            min_start = start
            break
        # if not valid, check if next solution for previous i-1 buses is valid for i-th bus
        start += solution_step
    # make sure step size is divisible by all previous bus IDs
    if solution_step % bus_id != 0:
        solution_step *= bus_id

print(min_start)
