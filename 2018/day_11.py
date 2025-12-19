import sys
import functools

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


@functools.cache
def get_row_sum(row, start, end):
    return sum(grid[x, row] for x in range(start, end))


def best_square(size):
    best = -10000
    winner = None
    for x in range(1, WIDTH + 1 - size):
        for y in range(1, HEIGHT + 1 - size):
            total = sum(get_row_sum(y + q, x, x + size) for q in range(size))
            if total > best:
                winner = (x, y)
                best = total

    return winner, best


print(best_square(3)[0])
last = -10000
best = -10000
for size in range(2, 300):
    new = best_square(size)
    if new[1] > best:
        winner = new[0] + (size,)
        best = new[1]
    if new[1] < last:
        break
    last = new[1]

print(",".join((str(part) for part in winner)))
