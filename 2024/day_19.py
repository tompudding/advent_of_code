import sys
import functools

with open(sys.argv[1], "r") as file:
    towels, patterns = file.read().split("\n\n")
    towels = [t.strip() for t in towels.split(",")]
    patterns = [p.strip() for p in patterns.splitlines()]


@functools.lru_cache
def possible(pattern):
    if not pattern:
        return True

    for towel in towels:
        if pattern.startswith(towel):
            if possible(pattern.removeprefix(towel)):
                return True
    return False


@functools.lru_cache
def num_ways(pattern):
    if not pattern:
        return 1

    total = 0
    for towel in towels:
        if pattern.startswith(towel):
            total += num_ways(pattern.removeprefix(towel))

    return total


patterns = [pattern for pattern in patterns if possible(pattern)]
print(len(patterns))

print(sum(num_ways(pattern) for pattern in patterns))
