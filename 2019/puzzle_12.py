import sys
import copy
import math


class Moon:
    def __init__(self, line):
        line = line.strip("<>")
        self.pos = [int(part.split("=")[1]) for part in line.split(",")]
        self.velocity = [0, 0, 0]

    def step_axis(self, axis):
        self.pos[axis] += self.velocity[axis]

    def equal_axis(self, other, axis):
        return self.pos[axis] == other.pos[axis] and self.velocity[axis] == other.velocity[axis]

    def energy(self):
        return sum(abs(p) for p in self.pos) * sum(abs(v) for v in self.velocity)

    def __repr__(self):
        return f"pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}> vel=<x={self.velocity[0]}, y={self.velocity[1]}, z={self.velocity[2]}>"


class System:
    def __init__(self, lines):
        self.moons = []

        for line in lines:
            self.moons.append(Moon(line.strip()))

    def step_axis(self, axis):
        # Gravity first
        for i, moon_a in enumerate(self.moons):
            for j in range(i + 1, len(self.moons)):
                moon_b = self.moons[j]
                if moon_a.pos[axis] == moon_b.pos[axis]:
                    continue

                diff = 1 if moon_a.pos[axis] > moon_b.pos[axis] else -1
                moon_a.velocity[axis] -= diff
                moon_b.velocity[axis] += diff

        for moon in self.moons:
            moon.step_axis(axis)

    def step(self):
        for axis in range(3):
            self.step_axis(axis)

    def energy(self):
        return sum(moon.energy() for moon in self.moons)

    def equal_axis(self, other, axis):
        for i in range(len(self.moons)):
            if not self.moons[i].equal_axis(other.moons[i], axis):
                return False

        return True

    def __repr__(self):
        out = []

        for moon in self.moons:
            out.append(repr(moon))

        out.append(f"energy={self.energy()}")
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    system = System(line for line in file)

orig_system = copy.deepcopy(system)

for i in range(1000):
    system.step()

print(system.energy())

system = copy.deepcopy(orig_system)

cycle_steps = [0, 0, 0]
for axis in range(3):
    while True:
        system.step_axis(axis)
        cycle_steps[axis] += 1

        if system.equal_axis(orig_system, axis):
            break

print(math.lcm(*cycle_steps))
