import sys


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concatenate(a, b):
    return int(str(a) + str(b))


def possible(result, total, numbers, num, operators):
    if total > result:
        return
    if len(numbers) == num:
        return total == result
    for operator in operators:
        if possible(result, operator(total, numbers[num]), numbers, num + 1, operators):
            return True


class Equation:
    def __init__(self, line):
        self.result, rest = line.split(":")
        self.result = int(self.result)
        self.numbers = [int(v) for v in rest.strip().split()]

    def possible(self, operators):
        return possible(self.result, self.numbers[0], self.numbers, 1, operators)


with open(sys.argv[1], "r") as file:
    equations = [Equation(line.strip()) for line in file]

valid = []
not_valid = []
for equation in equations:
    (valid if equation.possible((add, mul)) else not_valid).append(equation)

part_one = sum(equation.result for equation in valid)

print(part_one)

part_two = part_one + sum(
    equation.result for equation in not_valid if equation.possible((add, mul, concatenate))
)

print(part_two)
