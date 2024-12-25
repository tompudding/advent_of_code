import sys


class Lock:
    def __init__(self, lines):
        self.heights = [0 for i in range(len(lines[0]))]
        self.max_height = len(lines) - 1
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    continue
                self.heights[x] = y


class Key(Lock):
    def __init__(self, lines):
        super().__init__(lines[::-1])

    def fits(self, lock):
        return all(x + y < self.max_height for x, y in zip(self.heights, lock.heights))


with open(sys.argv[1], "r") as file:
    items = [chunk.splitlines() for chunk in file.read().split("\n\n")]

keys = []
locks = []

for item in items:
    if item[0].count("#") == len(item[0]):
        locks.append(Lock(item))
    elif item[-1].count("#") == len(item[-1]):
        keys.append(Key(item))
    else:
        raise BadItem()

print(sum(key.fits(lock) for key in keys for lock in locks))
