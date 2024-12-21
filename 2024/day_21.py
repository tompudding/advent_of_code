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
        # self.moves = {
        #     "A": (self.up, self.right, self.down, self.left),
        #     "<": (self.right, self.up, self.right),
        #     "v": (self.up, self.right, self.left),
        #     ">": (self.down, self.left, self.up),
        #     "^": (self.down, self.right, self.left),
        # }

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

    def write(self, code, start="A"):
        # The difference to the basic keypad is that this write function returns all possible codes
        button = start
        pos = self.button_to_pos[button]
        commands = []
        start = code
        code = list(code)

        while code:
            target_button = code.pop(0)
            target_pos = self.button_to_pos[target_button]

            diff = (target_pos[0] - pos[0], target_pos[1] - pos[1])
            moves = []
            if diff[0] < 0:
                moves.append(self.left)
            elif diff[0] > 0:
                moves.append(self.right)
            if diff[1] < 0:
                moves.append(self.up)
            elif diff[1] > 0:
                moves.append(self.down)

            # if there's only one move we can just take it
            if len(moves) == 1:
                new_commands, new_pos = moves[0](pos, target_pos)
                if not new_commands:
                    raise tim
                commands.extend(new_commands)
                commands.append("A")
                pos = new_pos
                continue

            # If there's two, we might still on have one ordering because one hits a gap

            extra_commands = []

            for move_set in moves, reversed(moves):
                current = pos
                current_commands = []
                for move in move_set:
                    new_commands, new_pos = move(current, target_pos)
                    if not new_commands:
                        break
                    current_commands.extend(new_commands)
                    current = new_pos
                else:
                    # If we didn't break it worked nicely
                    current_commands.append("A")
                    extra_commands.append(current_commands)
                    break

            commands.extend(extra_commands[0])
            pos = target_pos
            continue

        yield "".join(commands)


class ExhaustKeypad(Keypad):
    def write(self, code, start="A"):
        # The difference to the basic keypad is that this write function returns all possible codes
        button = start
        pos = self.button_to_pos[button]
        commands = []
        start = code
        code = list(code)

        while code:
            target_button = code.pop(0)
            target_pos = self.button_to_pos[target_button]

            diff = (target_pos[0] - pos[0], target_pos[1] - pos[1])
            moves = []
            if diff[0] < 0:
                moves.append(self.left)
            elif diff[0] > 0:
                moves.append(self.right)
            if diff[1] < 0:
                moves.append(self.up)
            elif diff[1] > 0:
                moves.append(self.down)

            # if there's only one move we can just take it
            if len(moves) == 1:
                new_commands, new_pos = moves[0](pos, target_pos)
                if not new_commands:
                    raise tim
                commands.extend(new_commands)
                commands.append("A")
                pos = new_pos
                continue

            # If there's two, we might still on have one ordering because one hits a gap

            extra_commands = []

            for move_set in moves, reversed(moves):
                current = pos
                current_commands = []
                for move in move_set:
                    new_commands, new_pos = move(current, target_pos)
                    if not new_commands:
                        break
                    current_commands.extend(new_commands)
                    current = new_pos
                else:
                    # If we didn't break it worked nicely
                    current_commands.append("A")
                    extra_commands.append(current_commands)

            if len(extra_commands) == 1:
                commands.extend(extra_commands[0])
                pos = target_pos
                continue

            # Otherwise we've got two choices and we want to try both

            for rest in self.write(code, start=self.pos_to_button[current]):
                for command_set in extra_commands:
                    # print("XX", "".join(commands), "|", "".join(command_set), "|", rest)
                    yield "".join(commands + command_set) + rest

            return

        yield "".join(commands)


numeric = ExhaustKeypad(["789", "456", "123", " 0A"])
directional = ExhaustKeypad([" ^A", "<v>"])
basic = Keypad([" ^A", "<v>"])
keypads = [numeric, directional, basic]


def command_all_robots(code, keypads, pos):
    if pos >= len(keypads):
        return len(code)

    best = 10**12
    for new_code in keypads[pos].write(code):
        new = command_all_robots(new_code, keypads, pos + 1)
        if new < best:
            best = new
            bc = new_code

    return best


with open(sys.argv[1], "r") as file:
    codes = [line.strip() for line in file]


print(sum(command_all_robots(code, keypads, 0) * int(code[:-1]) for code in codes))
