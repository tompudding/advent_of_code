import sys


class Brick:
    def __init__(self, space, desc):
        self.space = space
        c1, c2 = (x.split(",") for x in desc.split("~"))

        self.min, self.max = ([int(coord) for coord in pos] for pos in (c1, c2))

        self.register()

    def register(self):
        self.cubes = {
            (x, y, z)
            for x in range(self.min[0], self.max[0] + 1)
            for y in range(self.min[1], self.max[1] + 1)
            for z in range(self.min[2], self.max[2] + 1)
        }

        self.lowest_z = min(z for (x, y, z) in self.cubes)

        for cube in self.cubes:
            space[cube] = self

    def unsupported(self):
        return not self.drop_causes_collision(1)

    def drop_causes_collision(self, n, ignore=None):
        if self.lowest_z - n <= 0:
            return True

        for x, y, z in self.cubes:
            try:
                other = self.space[x, y, z - n]
            except KeyError:
                continue

            if other is not self and other is not ignore:
                return True
        return False

    def drop(self):
        to_drop = 0

        # We want to find how far we can go down before we're supported
        for drop in range(self.lowest_z + 1):
            if self.drop_causes_collision(drop):
                to_drop = drop - 1
                break

        assert to_drop > 0

        for cube in self.cubes:
            del self.space[cube]

        self.min[2] -= to_drop
        self.max[2] -= to_drop

        self.register()

    def __repr__(self):
        return f"Brick of {len(self.cubes)} cubes from {self.min} -> {self.max}"


with open(sys.argv[1], "r") as file:
    descs = [line.strip() for line in file]

space = {}

bricks = [Brick(space, desc) for desc in descs]

# Drop the falling bricks down
falling = sorted([brick for brick in bricks if brick.unsupported()], key=lambda brick: brick.lowest_z)

while falling:
    for brick in falling:
        brick.drop()

    falling = sorted([brick for brick in bricks if brick.unsupported()], key=lambda brick: brick.lowest_z)


disintegrates = 0

for brick in bricks:
    causes_fall = False

    for other in bricks:
        if other is brick:
            continue

        if not other.drop_causes_collision(n=1, ignore=brick):
            causes_fall = True
            break

    if not causes_fall:
        # Removing this brick doesn't cause anyting to fall
        disintegrates += 1

print(disintegrates)
