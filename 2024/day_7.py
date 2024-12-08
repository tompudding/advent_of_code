import sys


class InputError(Exception):
    pass


def div(a, b):
    if a % b != 0:
        raise InputError
    return a // b


def sub(a, b):
    return a - b


def split(a, b):
    if a == b:
        raise InputError

    while b:
        if ((a - b) % 10) != 0:
            raise InputError
        a //= 10
        b //= 10

    return a


def possible(result, total, numbers, num, operators):
    if total < result:
        return
    if len(numbers) == num:
        return total == result
    for operator in operators:
        try:
            if possible(result, operator(total, numbers[num]), numbers, num + 1, operators):
                return True
        except InputError:
            continue


class Equation:
    def __init__(self, line):
        self.result, rest = line.split(":")
        self.result = int(self.result)
        self.numbers = [int(v) for v in rest.strip().split()]

        # Actually let's go backwards!
        self.result, self.numbers = self.numbers[0], [self.result] + list(reversed(self.numbers))[:-1]

    def possible(self, operators):
        return possible(self.result, self.numbers[0], self.numbers, 1, operators)


with open(sys.argv[1], "r") as file:
    equations = [Equation(line.strip()) for line in file]

valid = []
not_valid = []
for equation in equations:
    (valid if equation.possible((div, sub)) else not_valid).append(equation)

part_one = sum(equation.numbers[0] for equation in valid)

print(part_one)

part_two = part_one + sum(
    equation.numbers[0] for equation in not_valid if equation.possible((div, sub, split))
)

print(part_two)
