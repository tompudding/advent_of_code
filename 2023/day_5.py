import sys
import bisect


class Range:
    def __init__(self, src, length):
        self.src = src
        self.length = length
        self.end = self.src + self.length

    def __lt__(self, other):
        return self.src < other.src

    def __repr__(self):
        return f"rnge:{self.src} - {self.end}"


class RangeMapping(Range):
    def __init__(self, src, dst, length):
        super().__init__(src, length)
        self.dst = dst
        self.adjust = dst - src

    def convert(self, input):
        if input < self.src or input >= self.src + self.length:
            return input

        return input + self.adjust

    def __repr__(self):
        return f"src:{self.src} - {self.src + self.length} dst:{self.dst} - {self.dst + self.length}"


class Point(Range):
    def __init__(self, num):
        self.src = num


class Ranges:
    def __init__(self, src_name=None, dst_name=None):
        self.src_name = src_name
        self.dst_name = dst_name

        # We'll store ranges sorted by start position
        self.ranges = []

    def add_range(self, new_range):
        bisect.insort_left(self.ranges, new_range)


class Mapping(Ranges):
    # A mapping is a set of ranges that can convert inputs
    def convert(self, input):
        point = Point(input)
        pos = bisect.bisect_right(self.ranges, point)
        if pos == 0:
            return input

        pos -= 1
        match = self.ranges[pos]

        return match.convert(input)

    def convert_range(self, input):
        output_ranges = Ranges()

        pos = 0

        to_convert = Range(input.src, input.length)

        while pos < len(self.ranges):
            if to_convert.src < self.ranges[pos].src:
                # Cut off the start
                cut_off_length = min(self.ranges[pos].src - to_convert.src, to_convert.length)

                output_ranges.add_range(Range(to_convert.src, cut_off_length))
                if cut_off_length == to_convert.length:
                    return output_ranges

                to_convert.src = self.ranges[pos].src
                to_convert.length -= cut_off_length
                continue
            elif to_convert.src >= self.ranges[pos].end:
                pos += 1
                continue
            elif to_convert.src >= self.ranges[pos].src and to_convert.src < self.ranges[pos].end:
                # There's an overlap, so do the conversion
                start = self.ranges[pos].convert(to_convert.src)
                # this is an inclusive end
                last = self.ranges[pos].convert(min(to_convert.end - 1, self.ranges[pos].end - 1))
                length = last - start + 1

                output_ranges.add_range(Range(start, length))
                to_convert.src += length
                if to_convert.length <= length:
                    return output_ranges
                to_convert.length -= length
                continue
            else:
                raise jim

        # if there's anything left in the input it should get added as is
        if to_convert.length > 0:
            output_ranges.add_range(to_convert)

        return output_ranges


class SeedRange(Ranges):
    def __init__(self):
        super().__init__("seed", "seed")

    def __repr__(self):
        out = [f"{len(self.ranges)} ranges:"]

        for rnge in self.ranges:
            out.append(f"{rnge.src} -> {rnge.end}")

        return "\n".join(out)


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


def apply_mappings_to_ranges(seed_ranges, mappings):
    for mapping in mappings:
        new_ranges = SeedRange()
        for rnge in seed_ranges.ranges:
            for new_range in mapping.convert_range(rnge).ranges:
                new_ranges.add_range(new_range)

        seed_ranges = new_ranges

    return seed_ranges


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

    current_mapping.add_range(RangeMapping(src, dst, length))

if current_mapping:
    mappings.append(current_mapping)

smallest = None
for seed in seeds:
    location = apply_mappings(seed)
    if smallest is None or location < smallest:
        smallest = location


print(smallest)

# For part 2 the seeds are ranges
smallest = None
for i in range(0, len(seeds), 2):
    seed_range = SeedRange()
    seed_range.add_range(Range(seeds[i], seeds[i + 1]))

    location_ranges = apply_mappings_to_ranges(seed_range, mappings)

    if smallest is None or location_ranges.ranges[0].src < smallest:
        smallest = location_ranges.ranges[0].src


print(smallest)
