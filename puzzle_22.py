import sys
import re


class Cube:
    def __init__(self, x, y, z):
        # Each of these x,y,z are inclusive ranges
        self.x = x
        self.y = y
        self.z = z

    def overlap(self, other):
        # This function will return two lists, the first of a cube of the overlap region, and the second all
        # the cubes that make up the non-overlapping regions of both. If there is no intersection both cubes
        # will be in the second list, and the first will be empty
        # print(f"OVERLAP {self} {other}")
        if (
            self.x[0] >= other.x[1]
            or self.x[1] < other.x[0]
            or self.y[0] >= other.y[1]
            or self.y[1] < other.y[0]
            or self.z[0] >= other.z[1]
            or self.z[1] < other.z[0]
        ):
            # print("No overlap")
            return None, [self, other]

        # Otherwise there's an overlap
        overlap = Cube(
            x=(max(self.x[0], other.x[0]), min(self.x[1], other.x[1])),
            y=(max(self.y[0], other.y[0]), min(self.y[1], other.y[1])),
            z=(max(self.z[0], other.z[0]), min(self.z[1], other.z[1])),
        )

        # Then we've got to split ourself and the other cube up to avoid the overlap region. We've got before and after in each of the 3 dimensions
        non_overlap = []

        for cube in (other,):
            # before in x
            for x_bounds in ((cube.x[0], overlap.x[0]), (overlap.x[1], cube.x[1])):
                if x_bounds[1] <= x_bounds[0]:
                    continue
                non_overlap.append(Cube(x_bounds, cube.y, cube.z))

            for y_bounds in ((cube.y[0], overlap.y[0]), (overlap.y[1], cube.y[1])):
                if y_bounds[1] <= y_bounds[0]:
                    continue
                non_overlap.append(Cube(overlap.x, y_bounds, cube.z))

            for z_bounds in ((cube.z[0], overlap.z[0]), (overlap.z[1], cube.z[1])):
                if z_bounds[1] <= z_bounds[0]:
                    continue
                non_overlap.append(Cube(overlap.x, overlap.y, z_bounds))
        return overlap, non_overlap

    def volume(self):
        return (self.x[1] - self.x[0]) * (self.y[1] - self.y[0]) * (self.z[1] - self.z[0])

    def __repr__(self):
        return f"x={self.x[0]}..{self.x[1]},y={self.y[0]}..{self.y[1]},z={self.z[0]}..{self.z[1]}"

    def __iter__(self):
        self.pos = [self.x[0], self.y[0], self.z[0]]
        self.ended = False
        return self

    def __next__(self):
        if self.ended:
            raise StopIteration
        out = tuple(self.pos)

        self.pos[2] += 1
        if self.pos[2] >= self.z[1]:
            self.pos[2] = self.z[0]
            self.pos[1] += 1
            if self.pos[1] >= self.y[1]:
                self.pos[1] = self.y[0]
                self.pos[0] += 1
                if self.pos[0] >= self.x[1]:
                    self.pos[0] = self.x[0]
                    self.ended = True

        return out


class Region:
    def __init__(self):
        self.on = []

    def turn_on(self, new_cube):
        new_cubes = [new_cube]

        for cube in self.on:
            overlap, non_overlap = new_cube.overlap(cube)

            if overlap is None:
                new_cubes.append(cube)
            else:
                new_cubes.extend(non_overlap)

        self.on = new_cubes

    def turn_off(self, new_cube):
        new_cubes = []

        for cube in self.on:
            overlap, non_overlap = new_cube.overlap(cube)

            if overlap is None:
                new_cubes.append(cube)
            else:
                new_cubes.extend(non_overlap)

        self.on = new_cubes

    def volume(self):
        return sum(cube.volume() for cube in self.on)


region = Region()

count = 0

with open(sys.argv[1], "r") as file:
    for line in file:
        match = re.match("(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)", line)
        if not match:
            continue
        op_str, *coords = match.groups()
        coords = [int(c) for c in coords]
        x_min, x_max, y_min, y_max, z_min, z_max = (int(c) for c in coords)

        # if any(abs(pos) > 50 for pos in coords):
        #    continue

        cube = Cube(x=(x_min, x_max + 1), y=(y_min, y_max + 1), z=(z_min, z_max + 1))

        if op_str == "on":
            region.turn_on(cube)
        else:
            region.turn_off(cube)

        count += 1
        # if count >= 2:
        #    break

# print("---")
# for cube in region.on:
#    print(cube)
print(region.volume())

# for cube in region.on:
#    print(cube)
#    print("---", cube, cube.volume())
#    # for point in cube:
#    #    print(point)
