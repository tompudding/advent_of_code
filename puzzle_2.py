import sys


class Position:
    def __init__(self):
        self.x = 0
        self.depth = 0
        self.handlers = {"forward": self.forward, "down": self.down, "up": self.up}

    def forward(self, amount):
        self.x += amount

    def down(self, amount):
        self.depth += amount

    def up(self, amount):
        self.depth -= amount

    def process_line(self, line):
        command, number = line.split()
        number = int(number)

        self.handlers[command](number)


class RealPosition(Position):
    def __init__(self):
        super().__init__()
        self.aim = 0

    def forward(self, amount):
        self.x += amount
        self.depth += amount * self.aim

    def down(self, amount):
        self.aim += amount

    def up(self, amount):
        self.aim -= amount


pos = Position()

with open(sys.argv[1], "r") as file:
    for line in file:
        pos.process_line(line.strip())

print(f"{pos.x=} {pos.depth=} {pos.x*pos.depth}")

pos = RealPosition()

with open(sys.argv[1], "r") as file:
    for line in file:
        pos.process_line(line.strip())

print(f"{pos.x=} {pos.depth=} {pos.x*pos.depth}")
