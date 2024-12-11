import sys
import collections


def stone_op(stone):
    stone_str = str(stone)
    num_digits = len(stone_str)

    if (len(stone_str) % 2) == 0:
        return [int(stone_str[: num_digits // 2]), int(stone_str[num_digits // 2 :])]
    elif stone == 0:
        return [1]
    else:
        return [stone * 2024]


with open(sys.argv[1], "r") as file:
    stones = [int(v) for v in file.read().strip().split()]

# We'll track what unique stones can possibly be made, and which stones they turn into
stone_maps = {n: stone_op(n) for n in stones}

new_maps = True
while new_maps:
    added = False
    new_maps = {}
    for n, m in stone_maps.items():
        new_maps |= {x: stone_op(x) for x in m if x not in stone_maps}

    stone_maps |= new_maps


def count_stones_at_step(stones, step):
    counts = {n: 1 for n in stones}

    for i in range(step):
        new_counts = collections.defaultdict(int)

        for n, count in counts.items():
            for new_value in stone_maps[n]:
                new_counts[new_value] += count
        counts = new_counts
    return sum(count for count in counts.values())


print(count_stones_at_step(stones, 25))
print(count_stones_at_step(stones, 75))
