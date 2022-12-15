import sys
import re


def man_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Sensor:
    def __init__(self, x, y, beacon_x, beacon_y):
        self.pos = (x, y)
        self.nearest_beacon = (beacon_x, beacon_y)
        self.distance = man_dist(self.pos, self.nearest_beacon)

    def no_beacon(self, output, line):
        # Start at the same position on the target line
        diff = abs(self.pos[1] - line)

        num = (self.distance - diff) * 2 + 1

        if num <= 0:
            return

        # print(self.pos, self.nearest_beacon, diff)

        # otherwise we have num ruled out on the target line starting at our x
        for x in range(num):

            output.add((self.pos[0] - (self.distance - diff) + x, line))

    def __contains__(self, pos):
        return man_dist(self.pos, pos) <= self.distance

    def perimeter(self, toward):
        diff = self.distance + 1
        top = [self.pos[0], self.pos[1] - diff]
        right = [self.pos[0] + diff, self.pos[1]]
        bottom = [self.pos[0], self.pos[1] + diff]
        left = [self.pos[0] - diff, self.pos[1]]
        if toward[0] >= self.pos[0] and toward[1] < self.pos[1]:
            # going up and to the right, so we start at the top and go down right
            step = [1, 1]
            start = top
            end = right
        elif toward[0] >= self.pos[0] and toward[1] >= self.pos[1]:
            step = [-1, 1]
            start = right
            end = bottom
        elif toward[0] < self.pos[0] and toward[1] >= self.pos[1]:
            step = [-1, -1]
            start = bottom
            end = left
        else:
            step = [1, -1]
            start = left
            end = top

        pos = start
        # print("xx", start, end, step)
        # print("xx", self.distance)
        while pos != end:
            yield pos
            pos[0] += step[0]
            pos[1] += step[1]
        yield end

    # def num_ruled_out(self):
    #    # return triangle(self.distance + 1) + triangle(self.distance) * 2 + triangle(self.distance - 1)
    #    return 4 * (self.distance + 1)


sensors = []
with open(sys.argv[1], "r") as file:
    for line in file:
        match = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        coords = [int(v) for v in match.groups()]
        sensors.append(Sensor(*coords))


if 0:
    ruled_out = set()
    pos = 2000000

    for sensor in sensors:
        sensor.no_beacon(ruled_out, pos)

    for sensor in sensors:
        if sensor.nearest_beacon in ruled_out:
            ruled_out.remove(sensor.nearest_beacon)

    print(len(ruled_out))

# Let's look at distances between each pair of sensors, and find ones whose distance is equal to their own
# size plus one

for i, sensor in enumerate(sensors):
    for j in range(i + 1, len(sensors)):
        other = sensors[j]

        distance = man_dist(sensor.pos, other.pos)

        if distance == sensor.distance + other.distance + 2:
            # We new inspect every square on their shared perimeter and test them against all the others. The
            # intersection of their perimeter is the perimeter of the smallest sensor in the direction of the
            # other one
            if sensor.distance < other.distance:
                source, target = sensor, other
            else:
                source, target = other, sensor
            # if not (i == 6 and j == 9):
            #    continue
            # print("wnk")
            for pos in source.perimeter(target.pos):
                # print(pos)
                # print(pos, [pos in s for s in sensors])
                if not any(pos in s for s in sensors):
                    print("bingo", i, j, pos)
                    print(pos[0] * 4000000 + pos[1])
                    break
        # print(distance, i, j, sensor.distance, other.distance)
