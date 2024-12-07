import sys


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def concatenate(a, b):
    return int(str(a) + str(b))


def increment(indices, num):
    for i in range(len(indices)):
        indices[i] += 1
        if indices[i] != num:
            break
        indices[i] = 0
    else:
        return True


class Equation:
    def __init__(self, line):
        self.result, rest = line.split(":")
        self.result = int(self.result)

        # We reverse the numbers so we compute from the right hand side
        self.numbers = [int(v) for v in rest.strip().split()]

    def possible(self, operators):
        indices = [0 for i in self.numbers[:-1]]

        while True:
            total = self.numbers[0]

            for i in range(len(indices)):
                operator = operators[indices[i]]
                total = operator(total, self.numbers[i + 1])

                if total == self.result and (i == len(indices) - 1):
                    return True
                if total > self.result:
                    break

            if increment(indices, len(operators)):
                return False


with open(sys.argv[1], "r") as file:
    equations = [Equation(line.strip()) for line in file]


print(sum(equation.result for equation in equations if equation.possible((add, mul))))
print(sum(equation.result for equation in equations if equation.possible((add, mul, concatenate))))
