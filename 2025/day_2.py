import sys
import functools


@functools.lru_cache
def divisors(n):
    out = []
    for i in range(1, (n // 2) + 1):
        if (n % i) == 0:
            out.append(i)
    return out


def chunks(iterable, length):
    for i in range(0, len(iterable), length):
        yield iterable[i : i + length]


class Range:
    def __init__(self, string):
        self.a, self.b = (int(x.strip()) for x in string.split("-"))

    def count(self, halves_only):
        count = set()

        for n in range(self.a, self.b + 1):
            str_n = str(n)

            if halves_only:
                if len(str_n) & 1:
                    continue
                substr_lengths = (len(str_n) // 2,)
            else:
                substr_lengths = divisors(len(str_n))

            for length in substr_lengths:
                if len(set(chunks(str_n, length))) == 1:
                    count.add(n)

        return sum(count)


with open(sys.argv[1]) as file:
    for line in file:
        ranges = [Range(part) for part in line.split(",")]
        break

print(sum(r.count(halves_only=True) for r in ranges))
print(sum(r.count(halves_only=False) for r in ranges))
