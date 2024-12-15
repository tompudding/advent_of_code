import sys
import intcode
import os
import collections

with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])


# Part 1
total = 0
positions = set()
for i in range(50):
    for j in range(50):
        program = intcode.IntCode(instructions, [i, j])

        try:
            program.resume()
        except intcode.Halted:
            pass

        total += program.output[0]
        if program.output[0]:
            positions.add((i, j))

print(total)


def get_beam(y):
    start = None
    end = None

    for x in range(int(0.6 * y), int(0.8 * y)):
        program = intcode.IntCode(instructions, [x, y])

        try:
            program.resume()
        except intcode.Halted:
            pass

        if start is None and program.output[0]:
            start = x

        elif not program.output[0] and start is not None:
            end = x
            return (start, end)

    print(y, start, end)
    raise Tim


# Let's just be stupid and go until we can fit 100 in, trigonometry is boring

y = 661
counts = collections.defaultdict(int)
while True:
    beam_on = get_beam(y)
    if beam_on[1] - beam_on[0] < 100:
        y += 1
        continue

    for x in range(*beam_on):
        counts[x] += 1

    if counts[beam_on[0]] >= 100 and counts[beam_on[0] + 99] >= 100:
        tc = (beam_on[0], (y - 99))
        break

    y += 1

print(tc[1] + tc[0] * 10000)
