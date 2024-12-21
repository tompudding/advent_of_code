import sys
from collections import defaultdict, Counter
import enum
import functools


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


def make_count(code):
    assert code[-1] == "A"
    return Counter([part for part in code[:-1].split("A")])


class Keypad:
    def __init__(self, lines):
        self.pos_to_button = {}
        self.gaps = set()
        self.counts = {}

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = (x, y)
                if char == " ":
                    self.gaps.add(p)
                    continue
                self.pos_to_button[p] = char

        self.button_to_pos = {v: k for k, v in self.pos_to_button.items()}

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

    def write_counts(self, counts):
        out = defaultdict(int)
        for part, start_count in counts.items():
            if part not in self.counts:
                code = list(self.write(part + "A"))[0]
                self.counts[part] = make_count(code)

            for out_part, count in self.counts[part].items():
                out[out_part] += count * start_count
        return out


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

            for move_set in (
                moves,
                reversed(moves),
            ):
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
            out = []
            for rest in self.write(tuple(code), start=self.pos_to_button[current]):
                for command_set in extra_commands:
                    # print("XX", "".join(commands), "|", "".join(command_set), "|", rest)
                    out.append("".join(commands + command_set) + rest)
            return out

            return

        out = ["".join(commands)]
        return out


numeric = ExhaustKeypad(["789", "456", "123", " 0A"])
directional = ExhaustKeypad([" ^A", "<v>"])
basic = Keypad([" ^A", "<v>"])
keypads = [numeric, basic, basic]


def command_all_robots(code, keypads, pos):
    if pos >= len(keypads):
        return len(code)

    best = 10**120
    for new_code in keypads[pos].write(code):
        new = command_all_robots(new_code, keypads, pos + 1)
        if new < best:
            best = new
            bc = new_code

    return best


def command_all_brobots(code, num):

    counts = make_count(code)

    for i in range(num):
        counts = basic.write_counts(counts)

    total = 0
    for k, value in counts.items():
        total += (len(k) + 1) * (value)
    return total


def command_all_robots_fast(code, num):

    best = 10**120
    for new_code in numeric.write(code):
        new = command_all_brobots(new_code, num)
        if new < best:
            best = new
            bc = new_code

    return best


with open(sys.argv[1], "r") as file:
    codes = [line.strip() for line in file]


print(sum(command_all_robots(code, keypads, 0) * int(code[:-1]) for code in codes))
print(sum(command_all_robots_fast(code, 2) * int(code[:-1]) for code in codes))

print(sum(command_all_robots_fast(code, 5) * int(code[:-1]) for code in codes))

print(len(basic.counts))

# 308848275370824 is too high
# 123381876968876 is too low
