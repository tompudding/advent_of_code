# (d+-(d**2-4*k)**0.5)/2

import sys
import math

with open(sys.argv[1], "r") as file:
    times_line, distances_line = file.readlines()[:2]

    times, distances = (
        [int(v) for v in line.split(":")[1].strip().split()] for line in (times_line, distances_line)
    )


def get_roots(k, d):
    return (d + (d**2 - 4 * k) ** 0.5) / 2, (d - ((d**2 - 4 * k) ** 0.5)) / 2


def get_winning_ways(distance, time):
    start, end = get_roots(distance, time)
    # If they are exact, they are ineligable
    if start == int(start):
        start = int(start) - 1
    else:
        start = int(start)

    end = int(end) + 1

    return start - end + 1


product = 1
for time, distance in zip(times, distances):
    product *= get_winning_ways(distance, time)

print(product)

# for part 2 we join them all
time, distance = (int("".join(line.split(":")[1].strip().split())) for line in (times_line, distances_line))

print(get_winning_ways(distance, time))
