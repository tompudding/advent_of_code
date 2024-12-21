import sys
from collections import defaultdict
import enum


class Directions(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


dir_name = {
    Directions.UP: "^",
    Directions.RIGHT: ">",
    Directions.LEFT: "<",
    Directions.DOWN: "v",
}


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


class Keypad:
    def __init__(self, lines):
        self.pos_to_button = {}
        self.gaps = set()

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = (x, y)
                if char == " ":
                    self.gaps.add(p)
                    continue
                self.pos_to_button[p] = char

        self.button_to_pos = {v: k for k, v in self.pos_to_button.items()}

        # self.moves = defaultdict(dict)

        # for pos, char in self.pos_to_button.items():
        #    for direction in Directions:
        #        new_pos = add(pos, direction.value)
        #        if new_pos in self.pos_to_button:
        #            self.moves[char][dir_name[direction]] = self.pos_to_button[new_pos]
        self.moves = {
            "A": (self.up, self.right, self.down, self.left),
            "<": (self.right, self.up, self.right),
            "v": (self.up, self.right, self.left),
            ">": (self.down, self.left, self.up),
            "^": (self.down, self.right, self.left),
        }

    def up(self, pos, target_pos):
        if target_pos[1] < pos[1]:
            # check there's no block
            for i in range(pos[1] - 1, target_pos[1] - 1, -1):
                if (pos[0], i) in self.gaps:
                    break
            else:
                # This is good, we can step the whole way
                step = Directions.UP
                commands = [dir_name[step]] * (pos[1] - target_pos[1])
                pos = (pos[0], target_pos[1])
                return commands, pos
        return None, None

    def right(self, pos, target_pos):
        if target_pos[0] > pos[0]:
            # check there's no block
            for i in range(pos[0] + 1, target_pos[0] + 1):
                if (i, pos[1]) in self.gaps:
                    break
            else:
                # This is good, we can step the whole way
                step = Directions.RIGHT
                commands = [dir_name[step]] * (target_pos[0] - pos[0])
                pos = (target_pos[0], pos[1])
                return commands, pos
        return None, None

    def left(self, pos, target_pos):
        if target_pos[0] < pos[0]:
            # check there's no block
            for i in range(pos[0] - 1, target_pos[0] - 1, -1):
                if (i, pos[1]) in self.gaps:
                    break
            else:
                # This is good, we can step the whole way
                step = Directions.LEFT
                commands = [dir_name[step]] * (pos[0] - target_pos[0])
                pos = (target_pos[0], pos[1])
                return commands, pos
        return None, None

    def down(self, pos, target_pos):
        print("A", pos, target_pos)
        if target_pos[1] > pos[1]:
            # check there's no block
            for i in range(pos[1] + 1, target_pos[1] + 1):
                if (pos[0], i) in self.gaps:
                    break
            else:
                # This is good, we can step the whole way
                step = Directions.DOWN
                commands = [dir_name[step]] * (target_pos[1] - pos[1])
                pos = (pos[0], target_pos[1])
                return commands, pos
        return None, None

    def write(self, code):
        # I think we always start a 'A'
        button = "A"
        pos = self.button_to_pos[button]
        commands = []
        start = code
        code = list(code)

        while code:
            target_button = code.pop(0)
            target_pos = self.button_to_pos[target_button]
            while pos != target_pos:
                # It doesn't matter how we get there, except we need to not go off the edge.
                # LOL it does matter because we need to press the same button as much as possible to keep subsequent commands short.
                # So we'll move always the entire way in one direction, whichever one doesn't hit a block.
                # Also UP and right are closes to A, followed by down, then left is furthest away. Oh god this could get complicated.
                # Instead let's do it in order of proximity to the last thing we typed
                print(self.pos_to_button)
                button = self.pos_to_button[pos]
                try:
                    moves = self.moves[button]
                except KeyError:
                    moves = self.up, self.down, self.right, self.left
                for move in moves:
                    new_commands, new_pos = move(pos, target_pos)
                    if new_commands:
                        commands.extend(new_commands)
                        pos = new_pos
                        print(pos, move)
                        break
                else:
                    raise Ohno

            # Then we need to punch A
            commands.append("A")
        out = "".join(commands)

        print(f"{start} -> {out}")
        return out


numeric = Keypad(["789", "456", "123", " 0A"])
directional = Keypad([" ^A", "<v>"])
keypads = [numeric, directional, directional]


def command_all_robots(code):
    for keypad in keypads:
        code = keypad.write(code)
        print(code)

    return code


with open(sys.argv[1], "r") as file:
    codes = [line.strip() for line in file]

total = 0
for code in codes:
    command = command_all_robots(code)
    print(len(command))
    total += len(command) * int(code[:-1])
print(total)

# print(sum(len(command_all_robots(code)) * int(code[:-1]) for code in codes))

# 228938 is too high
# 225066 is too high
