import sys


# Make the number a class so it can be hashed in a set by its unique id rather than its value, otherwise we
# might confuse numbers with different positions but the same value
class Number:
    def __init__(self, num):
        self.value = num


symbols = {}
numbers = {}

with open(sys.argv[1], "r") as file:
    for row, line in enumerate(file):
        line = line.strip()
        pos = 0
        while pos < len(line):
            if "." == line[pos]:
                pos += 1
            elif line[pos].isdigit():
                for next_pos in range(pos + 1, len(line) + 1):
                    if next_pos == len(line) or not line[next_pos].isdigit():
                        break
                num = Number(int(line[pos:next_pos]))
                for i in range(pos, next_pos):
                    numbers[(i, row)] = num
                pos = next_pos
            else:
                symbols[(pos, row)] = line[pos]
                pos += 1

neighbours = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)]
symbol_adjacent = {(pos[0] + x, pos[1] + y) for pos in symbols for (x, y) in neighbours}

parts = {numbers[part_pos] for part_pos in symbol_adjacent & numbers.keys()}
print(sum(part.value for part in parts))

gear_ratio = 0
stars = {pos: sym for pos, sym in symbols.items() if sym == "*"}

for pos in stars:
    adjacent = {(pos[0] + x, pos[1] + y) for (x, y) in neighbours}
    adjacent = {numbers[part_pos] for part_pos in adjacent & numbers.keys()}
    if len(adjacent) != 2:
        continue

    gear_ratio += adjacent.pop().value * adjacent.pop().value

print(gear_ratio)
