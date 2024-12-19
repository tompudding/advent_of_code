import sys
import functools

with open(sys.argv[1], "r") as file:
    towels, patterns = file.read().split("\n\n")
    towels = [t.strip() for t in towels.split(",")]
    patterns = [p.strip() for p in patterns.splitlines()]


@functools.lru_cache
def count(pattern, collect):
    if pattern:
        return collect(
            count(pattern.removeprefix(towel), collect) for towel in towels if pattern.startswith(towel)
        )
    return True


patterns = [pattern for pattern in patterns if count(pattern, any)]
print(len(patterns))
print(sum(count(pattern, sum) for pattern in patterns))
