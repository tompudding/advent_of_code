import sys
import re


class Sensor:
    def __init__(self, x, y, beacon_x, beacon_y):
        self.pos = (x, y)
        self.nearest_beacon = (beacon_x, beacon_y)
        self.distance = abs(beacon_x - x) + abs(beacon_y - y)

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


sensors = []
with open(sys.argv[1], "r") as file:
    for line in file:
        match = re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        coords = [int(v) for v in match.groups()]
        sensors.append(Sensor(*coords))


ruled_out = set()
pos = 2000000

for sensor in sensors:
    sensor.no_beacon(ruled_out, pos)

for sensor in sensors:
    if sensor.nearest_beacon in ruled_out:
        ruled_out.remove(sensor.nearest_beacon)

print(len(ruled_out))
