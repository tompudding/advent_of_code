import sys
import re
from fractions import Fraction


class Equation:
    def __init__(self, line):
        match = re.search("[^\d]*(\d+), [^\d]*(\d+)$", line.strip())
        self.x = Fraction(match.groups()[0])
        self.y = Fraction(match.groups()[1])

    def __repr__(self):
        return f"{self.x} + {self.y}"


class ClawMachine:
    def __init__(self, lines):
        self.a, self.b, self.K = (Equation(line.strip()) for line in lines)

    def get_button_presses(self, limit=None):
        # A*x_a + B*y_a = K_A
        # A*x_b + B*y_b = K_B
        #

        # b = (self.a.x * (self.K.x * self.b.x - self.K.y)) / (self.a.y * self.b.y)

        b = (self.K.y - ((self.a.y * self.K.x) / self.a.x)) / (self.b.y - ((self.b.x * self.a.y) / self.a.x))

        if not b.is_integer() or limit is not None and b > limit:
            return 0

        a = (self.K.x - self.b.x * b) / self.a.x

        if not a.is_integer() or limit is not None and a > limit:
            return 0

        num_presses = a * 3 + b
        return num_presses

    def __repr__(self):
        return f"{self.a} {self.b} K={self.K}"


with open(sys.argv[1], "r") as file:
    machines = [ClawMachine(lines.splitlines()) for lines in file.read().split("\n\n")]

print(sum(machine.get_button_presses(limit=100) for machine in machines))

for machine in machines:
    machine.K.x += 10000000000000
    machine.K.y += 10000000000000

print(sum(machine.get_button_presses() for machine in machines))

# 951 is too low
# 15708 is too low
