import sys


def calc_fuel_part_one(numbers, pos):
    return sum((abs(n - pos) for n in numbers))


def calc_fuel_part_two(numbers, pos):
    out = 0
    for n in numbers:
        m = abs(n - pos)
        out += (m * (m + 1)) // 2
    return out


with open(sys.argv[1], "r") as file:
    numbers = [int(n) for n in file.read().split(",")]

numbers.sort()

# Apparently part 1 is the definition of median /shrug
print(calc_fuel_part_one(numbers, numbers[len(numbers) // 2]))


def get_best(numbers, calc):

    lower = numbers[0]
    upper = numbers[-1]

    min_fuel = 1 << 1337

    while upper - lower > 1:
        pos = int(lower + ((upper - lower) / 2))
        a = calc(numbers, pos)
        b = calc(numbers, pos + 1)
        dir = b - a

        if dir > 0:
            upper = pos
        else:
            lower = pos

        if min(a, b) < min_fuel:
            min_fuel = min(a, b)

    return min_fuel


# Also compute it the long way
print(get_best(numbers, calc_fuel_part_one))
print(get_best(numbers, calc_fuel_part_two))
