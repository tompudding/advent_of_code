import sys
import bisect


class Range:
    def __init__(self, src, dst, length):
        self.src = src
        self.dst = dst
        self.length = length
        self.adjust = dst - src

    def convert(self, input):
        if input < self.src or input >= self.src + self.length:
            return input

        return input + self.adjust

    def __lt__(self, other):
        return self.src < other.src

    def __repr__(self):
        return f"src:{self.src} - {self.src + self.length} dst:{self.dst} - {self.dst + self.length}"


class Point(Range):
    def __init__(self, num):
        self.src = num


class Mapping:
    def __init__(self, src_name, dst_name):
        self.src_name = src_name
        self.dst_name = dst_name

        # We'll store ranges sorted by start position
        self.ranges = []

    def add_range(self, new_range):
        bisect.insort_left(self.ranges, new_range)

    def convert(self, input):
        point = Point(input)
        pos = bisect.bisect_right(self.ranges, point)
        if pos == 0:
            return input

        pos -= 1
        match = self.ranges[pos]

        return match.convert(input)


with open(sys.argv[1], "r") as file:
    lines = file.readlines()

    seeds = [int(seed) for seed in lines[0].split(": ")[1].split()]

current_mapping = None
mappings = []


def apply_mappings(seed):
    current = seed

    for mapping in mappings:
        tmp = mapping.convert(current)
        # print(f"convert {current} -> {tmp}")
        current = tmp

    return current


for line in lines[1:]:
    line = line.strip()
    if not line:
        continue

    if " map" in line:
        name = line.split()[0]
        src_name, hyphen, dst_name = line.split("-")
        if current_mapping:
            mappings.append(current_mapping)
        current_mapping = Mapping(src_name, dst_name)
        continue

    dst, src, length = (int(part) for part in line.split())

    current_mapping.add_range(Range(src, dst, length))

if current_mapping:
    mappings.append(current_mapping)

smallest = None
for seed in seeds:
    location = apply_mappings(seed)
    if smallest is None or location < smallest:
        smallest = location
    print(seed, location)

print(smallest)
