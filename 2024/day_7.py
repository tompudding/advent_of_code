import sys


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concatenate(a, b):
    return int(str(a) + str(b))


def possible(result, total, numbers, operators):
    if len(numbers) == 0:
        return total == result
    for operator in operators:
        new_total = operator(total, numbers[0])

        if new_total > result:
            continue

        success = possible(result, new_total, numbers[1:], operators)
        if success:
            return success


class Equation:
    def __init__(self, line):
        self.result, rest = line.split(":")
        self.result = int(self.result)

        # We reverse the numbers so we compute from the right hand side
        self.numbers = [int(v) for v in rest.strip().split()]

    def possible(self, operators):
        return possible(self.result, self.numbers[0], self.numbers[1:], operators)


with open(sys.argv[1], "r") as file:
    equations = [Equation(line.strip()) for line in file]

valid = []
not_valid = []
for eq in equations:
    if eq.possible((add, mul)):
        valid.append(eq)
    else:
        not_valid.append(eq)

part_one = sum(equation.result for equation in valid)

print(part_one)

part_two = part_one + sum(
    equation.result for equation in not_valid if equation.possible((add, mul, concatenate))
)

print(part_two)
