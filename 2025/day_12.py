import sys


class Shape:
    def __init__(self, lines):
        self.points = {(x, y) for y, row in enumerate(lines) for x, char in enumerate(row) if char == "#"}


class Requirement:
    def __init__(self, line):
        area, numbers = line.split(": ", maxsplit=1)
        self.width, self.height = (int(x) for x in area.split("x"))
        self.area = self.width * self.height
        self.requirements = {shape: int(number) for shape, number in enumerate(numbers.split())}

    def technically_possible(self, shapes):
        # If there isn't enough room for all the set bits, don't even bother
        required_area = sum(len(shapes[shape].points) * num for shape, num in self.requirements.items())

        return required_area < self.width * self.height

    def trivial(self):
        # How many complete 3x3 blocks do we have?
        width = 3 * (self.width // 3)
        height = 3 * (self.height // 3)
        blocks_area = width * height
        return blocks_area >= sum(self.requirements.values())


with open(sys.argv[1]) as file:
    parts = file.read().split("\n\n")

shapes = [Shape(part.split("\n")) for part in parts[:-1]]
requirements = [line.strip() for line in parts[-1].split("\n")]
requirements = [Requirement(line) for line in requirements if line]

# Let's throw away any that are clearly impossible
requirements = [r for r in requirements if r.technically_possible(shapes)]

# Now we can remove any that area trivially possible
trivial = []
tricksy = []

for requirement in requirements:
    (trivial if requirement.trivial() else tricksy).append(requirement)

# Oh they're all trivial. I'm glad I spent a week thinking about this >.<

if tricksy:
    print("This one is tricksy!")
else:
    print(len(trivial))
