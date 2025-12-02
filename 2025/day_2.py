import sys
import functools


@functools.lru_cache
def divisors(n):
    out = []
    for i in range(1, (n // 2) + 1):
        if (n % i) == 0:
            out.append(i)
    return out


class Range:
    def __init__(self, start, end):
        self.a_str, self.b_str = start, end
        self.a = int(self.a_str)
        self.b = int(self.b_str)

        assert len(self.a_str) == len(self.b_str)

    def count(self, halves_only):
        count = set()

        # The lengths of our strings are the same by construction.
        if halves_only:
            substr_lengths = (len(self.a_str) // 2,)
            if len(self.a_str) & 1:
                return 0
        else:
            substr_lengths = divisors(len(self.a_str))

        for length in substr_lengths:

            lower = int(self.a_str[:length])
            upper = int(self.b_str[:length])
            repeats = len(self.a_str) // length

            for n in range(lower, upper + 1):
                target = int(str(n) * repeats)
                if target >= self.a and target <= self.b:
                    count.add(target)

        return sum(count)


ranges = []
with open(sys.argv[1]) as file:
    for line in file:
        for num_range in line.split(","):
            start, end = (val.strip() for val in num_range.split("-"))

            if len(start) == len(end):
                ranges.append(Range(start, end))
            else:
                # When they're not the same length split it into two regions for my sanity
                ranges.append(Range(start, "9" * len(start)))
                ranges.append(Range("1" + "0" * len(start), end))
        break

print(sum(r.count(halves_only=True) for r in ranges))
print(sum(r.count(halves_only=False) for r in ranges))
