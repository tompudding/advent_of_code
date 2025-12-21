import sys
import itertools


def parse_mask(mask):
    out = 0
    for i in range(len(mask)):
        if mask[i] == "#":
            out |= 1 << i
    return out


class PlantTunnel:
    def __init__(self, state, rules):
        self.state = state.split(": ")[1]
        self.state = {i for i, char in enumerate(self.state) if char == "#"}

        # The important thing is that no plants makes no plants, so we only have to consider each plant, and
        # its surroundings
        self.makes_plant = set()
        self.min = min(self.state)
        self.max = max(self.state)

        for line in rules.splitlines():
            mask, result = line.strip().split(" => ")
            if result != "#":
                continue
            self.makes_plant.add(parse_mask(mask))

    def step(self):
        new = set()

        possibles = set()
        for plant in self.state:
            possibles |= set(range(plant - 2, plant + 3))

        for pos in possibles:
            mask = 0
            for place in range(pos - 2, pos + 3):
                if place in self.state:
                    mask |= 1 << (place - (pos - 2))

            if mask in self.makes_plant:
                new.add(pos)
                self.min = min(pos, self.min)
                self.max = max(pos, self.max)

        self.state = new

    def __repr__(self):
        return "".join(["#" if i in self.state else "." for i in range(self.min, self.max + 1)])


with open(sys.argv[1]) as file:
    parts = file.read().split("\n\n")

tunnel = PlantTunnel(parts[0], parts[1])
tunnel.step()
# Part 1
print(sum(tunnel.state))

tunnel = PlantTunnel(parts[0], parts[1])
# For Part 2 it looks like eventually it stabilises with everything apart from everything else and then just
# walks to the side, so step it until that happens
for step in range(0x100):
    tunnel.step()
    distance = min(b - a for a, b in itertools.pairwise(sorted(tunnel.state)))
    if distance >= 5:
        step += 1
        break
else:
    raise OhDear()

target_steps = 50000000000
remaining_steps = target_steps - step
total = sum(tunnel.state) + remaining_steps * len(tunnel.state)
print(total)
