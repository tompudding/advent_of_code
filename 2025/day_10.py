import numpy as np
import scipy.optimize
import sys


def parse_button(text):
    return [int(v) for v in text.strip("()").split(",")]


def button_to_value(button):
    return sum(1 << i for i in button)


def parse_desired(desired):
    desired = desired.strip("[]")
    return sum(1 << i if char == "#" else 0 for i, char in enumerate(desired))


def convert_buttons(data, num):
    return np.array([[1 if i in button else 0 for button in data] for i in range(num)])


def bits_set(x, n):
    return sum((x >> i) & 1 for i in range(n))


class Machine:
    def __init__(self, line):
        desired, rest = line.split(None, maxsplit=1)
        buttons, joltage = rest.split("{")
        self.joltage = np.array([int(v) for v in joltage.strip("}").split(",")])
        self.buttons = [parse_button(part) for part in buttons.split()]
        self.button_values = [button_to_value(button) for button in self.buttons]
        self.desired = parse_desired(desired)
        self.button_equations = convert_buttons(self.buttons, len(self.joltage))

    def press_result(self, pattern):
        out = 0
        for i in range(len(self.buttons)):
            if (pattern >> i) & 1:
                out ^= self.button_values[i]
        return out

    def min_presses(self):
        density = len(self.buttons)
        # This is inefficient, we could do this in order of density and stop at the first hit but I can't be
        # bothered
        for press_pattern in range(1 << len(self.buttons)):
            press_result = self.press_result(press_pattern)
            if press_result == self.desired:
                density = min(density, bits_set(press_pattern, len(self.buttons)))

        return density

    def min_joltage_presses(self):
        # Scipi's linprog does exactly where we want, it minimises the function C over the solution
        result = scipy.optimize.linprog(
            c=np.array([1 for i in range(len(self.button_equations[0]))]),
            A_eq=self.button_equations,
            b_eq=self.joltage,
            integrality=1,
        )
        # Adding the values for result.x doesn't always give result.fun. Floating point errors?
        # We can check that taking int on it is at least mostly accurate
        assert (result.fun - int(result.fun)) < 0.01
        return int(result.fun)


with open(sys.argv[1]) as file:
    machines = [Machine(line.strip()) for line in file]


print(sum(machine.min_presses() for machine in machines))
print(sum(machine.min_joltage_presses() for machine in machines))
