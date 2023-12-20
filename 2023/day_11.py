import sys

grid = {}
galaxies = []
galaxy_rows = set()
galaxy_cols = set()

empty_rows = set()
empty_cols = set()

width = 0
height = 0

with open(sys.argv[1], "r") as file:
    for y, line in enumerate(file):
        if y + 1 > height:
            height = y + 1
        for x, char in enumerate(line.strip()):
            if x + 1 > width:
                width = x + 1
            grid[x, y] = char

            if char == "#":
                galaxies.append((x, y))
                galaxy_rows.add(y)
                galaxy_cols.add(x)

empty_rows = set(range(height)) - galaxy_rows
empty_cols = set(range(width)) - galaxy_cols

total = 0


def get_distances(multiplier):
    total = 0

    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            a = galaxies[i]
            b = galaxies[j]

            distance = 0

            for x in range(min(a[0], b[0]) + 1, max(a[0], b[0]) + 1):
                distance += multiplier if x in empty_cols else 1

            for y in range(min(a[1], b[1]) + 1, max(a[1], b[1]) + 1):
                distance += multiplier if y in empty_rows else 1

            total += distance

    return total


print(get_distances(2))
print(get_distances(1000000))
