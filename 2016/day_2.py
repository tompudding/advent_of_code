import sys
import enum
from collections import defaultdict


class Directions(enum.Enum):
    U = (0, -1)
    R = (1, 0)
    D = (0, 1)
    L = (-1, 0)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def build_keypad(lines):
    keypad = {}

    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == " ":
                continue
            keypad[(x, y)] = char

    moves = defaultdict(dict)

    for pos, char in keypad.items():
        for direction in Directions:
            new_pos = add(pos, direction.value)
            if new_pos in keypad:
                moves[char][direction.name] = keypad[new_pos]
    return moves


def follow_command(moves, command, pos):
    for step in command:
        try:
            pos = moves[pos][step]
        except KeyError:
            continue
    return pos


def get_code(moves, commands):
    code = []
    pos = "5"

    for command in commands:
        pos = follow_command(moves, command, pos)
        code.append(pos)

    return "".join(code)


with open(sys.argv[1], "r") as file:
    commands = [line.strip() for line in file]

part_one_moves = build_keypad(["123", "456", "789"])
part_two_moves = build_keypad(
    [
        "   1    ",
        "  234",
        " 56789",
        "  ABC",
        "   D",
    ]
)


print(get_code(part_one_moves, commands))
print(get_code(part_two_moves, commands))
