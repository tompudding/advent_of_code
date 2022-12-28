import sys


def op(n):
    return n // 3 - 2


def op_part2(n):
    last = op(n)
    total = last

    while last > 0:
        last = op(last)
        if last <= 0:
            break
        total += last

    return total


with open(sys.argv[1], "r") as file:
    fuels = [int(lines.strip()) for lines in file]

print(sum(op(fuel) for fuel in fuels))
print(sum(op_part2(fuel) for fuel in fuels))
