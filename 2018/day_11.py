import sys

# rack_id = x+10
# power = (rack_id*y + serial)*rack_id = y*(x**2 + 20x + 100) + (x+10)*serial


def power_level(x, y, serial):
    rack_id = x + 10
    power = (rack_id * y + serial) * rack_id
    power = ((power // 100) % 10) - 5
    return power


with open(sys.argv[1], "r") as file:
    serial = int(file.read().strip())

WIDTH = 300
HEIGHT = 300

grid = {(x, y): power_level(x, y, serial) for x in range(1, WIDTH + 1) for y in range(1, WIDTH + 1)}


def best_square(size):
    best = 0
    winner = None
    for x in range(1, WIDTH + 1 - size):
        for y in range(1, HEIGHT + 1 - size):
            total = sum(grid[x + p, y + q] for p in range(size) for q in range(size))
            if total > best:
                winner = (x, y)
                best = total

    return winner


print(best_square(200))
