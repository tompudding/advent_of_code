import sys
import math
import cmath

asteroids = set()

height = 0
with open(sys.argv[1], "r") as file:
    for row, line in enumerate(file):
        asteroids |= {(col, row) for col, ch in enumerate(line.strip()) if ch == "#"}
        height += 1
    width = len(line.strip())


def get_visible(asteroids, asteroid):
    invisible = {asteroid}

    for other in asteroids:
        if other is asteroid:
            continue

        # we delete all the multiples of difference
        diff = (other[0] - asteroid[0], other[1] - asteroid[1])
        gcd = math.gcd(diff[0], diff[1])
        diff = (diff[0] // gcd, diff[1] // gcd)

        pos = other

        while pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height:
            pos = (pos[0] + diff[0], pos[1] + diff[1])
            invisible.add(pos)

    return asteroids - invisible


visibility = sorted(
    [(asteroid, len(get_visible(asteroids, asteroid))) for asteroid in asteroids], key=lambda x: x[1]
)

laser, num_visible = visibility[-1]

# Part 1
print(num_visible)

current_asteroids = {asteroid for asteroid in asteroids}
num_destroyed = 0

nth_destroyed = 200

while num_destroyed < nth_destroyed:
    to_destroy = get_visible(current_asteroids, laser)

    current_asteroids -= to_destroy

    if num_destroyed + len(to_destroy) < nth_destroyed:
        # We don't care about the angles yet
        num_destroyed += len(to_destroy)
        continue

    # Get the angles for each of these, measured from the top
    destroy_order = []
    for other in to_destroy:
        diff = (other[0] - laser[0], laser[1] - other[1])
        distance, angle = cmath.polar(diff[0] + diff[1] * 1j)
        angle = math.pi * 0.5 - angle
        if angle < 0:
            angle += math.pi * 2
        destroy_order.append((other, angle))

    destroy_order.sort(key=lambda x: x[1])

    winner = destroy_order[nth_destroyed - (num_destroyed + 1)][0]
    break

print(winner[0] * 100 + winner[1])
