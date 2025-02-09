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


class Keypad:
    def __init__(self, lines):
        self.pos_to_button = {}
        self.button_to_pos = {}
        self.gaps = set()
        self.counts = {}

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                p = (x, y)
                if char == " ":
                    self.gaps.add(p)
                    continue
                self.pos_to_button[p] = char
                self.button_to_pos[char] = p

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

    @functools.cache
    def get_path(self, start, end):
        pos = self.button_to_pos[start]
        end_pos = self.button_to_pos[end]
        commands = []

        diff = (end_pos[0] - pos[0], end_pos[1] - pos[1])

        moves = []
        if diff[0] < 0:
            moves.append(self.left)
        elif diff[0] > 0:
            moves.append(self.right)
        if diff[1] < 0:
            moves.append(self.up)
        elif diff[1] > 0:
            moves.append(self.down)

        # If there's two, we might still on have one ordering because one hits a gap

        extra_commands = []

        for move_set in (
            moves,
            reversed(moves),
        ):
            current = pos
            current_commands = []
            for move in move_set:
                new_commands, new_pos = move(current, end_pos)
                if not new_commands:
                    break
                current_commands.extend(new_commands)
                current = new_pos
            else:
                # If we didn't break it worked nicely
                current_commands.append("A")
                extra_commands.append(current_commands)

        return [commands + command_set for command_set in extra_commands]

    def write(self, code, start="A"):
        # This writes the full list of commands needed to punch in code

        button = start
        start = code
        code = list(code)

        while code:
            target_button = code.pop(0)
            command_set = self.get_path(button, target_button)
            button = target_button

            out = []
            if not code:
                return ["".join(cs) for cs in command_set]

            for rest in self.write(tuple(code), start=target_button):
                for cs in command_set:
                    out.append("".join(cs) + rest)

            return out

        raise BadCode()


numeric = Keypad(["789", "456", "123", " 0A"])
directional = Keypad([" ^A", "<v>"])


@functools.cache
def total_keypad_paths(code, num):
    current = "A"
    total = 0

    if num == 0:
        return len(code)

    for i in range(len(code)):
        next_item = code[i]
        if current == next_item:
            total += 1
            continue

        total += min(
            total_keypad_paths(tuple(path), num - 1) for path in directional.get_path(current, next_item)
        )
        current = next_item

    return total


def command_all_robots(code, num):
    best = 10**120
    for new_code in numeric.write(code):

        current = "A"
        total = 0

        for i in range(len(new_code)):
            next_item = new_code[i]
            if current == next_item:
                total += 1
                continue

            # Now we consider the different ways of going from current to next_item. There are either 1 or 2
            # of them, but for each one, we descend into asking "if we used that one, how many ways would
            # there be for the rest of the code?". We can recurse for that and cache everything because each
            # step of the path leaves the higher robots at A

            total += min(
                total_keypad_paths(tuple(path), num - 1) for path in directional.get_path(current, next_item)
            )
            current = next_item

        if total < best:
            best = total

    return best


with open(sys.argv[1], "r") as file:
    codes = [line.strip() for line in file]

print(sum(command_all_robots(code, 2) * int(code[:-1]) for code in codes))
print(sum(command_all_robots(code, 25) * int(code[:-1]) for code in codes))
