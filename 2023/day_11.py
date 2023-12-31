import sys

galaxies = []
galaxy_rows = set()
galaxy_cols = set()

with open(sys.argv[1], "r") as file:
    for y, line in enumerate(file):
        for x, char in enumerate(line.strip()):
            if char == "#":
                galaxies.append((x, y))
                galaxy_rows.add(y)
                galaxy_cols.add(x)


def get_distances(multiplier):
    total = 0

    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            a = galaxies[i]
            b = galaxies[j]

            distance = 0

            for x in range(min(a[0], b[0]) + 1, max(a[0], b[0]) + 1):
                distance += multiplier if x not in galaxy_cols else 1

            for y in range(min(a[1], b[1]) + 1, max(a[1], b[1]) + 1):
                distance += multiplier if y not in galaxy_rows else 1

            total += distance

    return total


print(get_distances(2))
print(get_distances(1000000))
