import sys
from utils import Point3D
import functools


@functools.total_ordering
class Cube:
    # vectors to each of the faces.
    face_vectors = [
        Point3D(*p)
        for p in (
            (1, 0, 0),
            (0, 1, 0),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        )
    ]

    def __init__(self, centre):
        self.centre = centre
        self.centre_face_coords = centre * 2

        self.faces = [self.centre_face_coords + vector for vector in self.face_vectors]
        self.faces_set = set(self.faces)

    def neighbours(self):
        for vector in self.face_vectors:
            yield Cube(self.centre + vector)

    def __eq__(self, other):
        return self.centre == other.centre

    def __lt__(self, other):
        return self.centre < other.centre

    def __repr__(self):
        return f"Cube at {self.centre}"

    def __hash__(self):
        return hash(self.centre)


def out_of_bounds(cube, bounds):
    for i, coord in enumerate(cube.centre):
        if coord > bounds[i][1] + 1 or coord < bounds[i][0] - 1:
            # print(f'For cube "{cube}" we find coord {i}:{coord} is out of bounds {bounds}')
            return True
    return False


def get_surface_area(cubes):
    surface_area = {}

    for cube in cubes:
        for face in cube.faces:
            try:
                surface_area[face] += 1
            except KeyError:
                surface_area[face] = 1

    return set([face for face, count in surface_area.items() if count == 1])


cubes = []
with open(sys.argv[1], "r") as file:
    for line in file:
        cubes.append(Cube(Point3D(*[int(v) for v in line.strip().split(",")])))

surface_area = get_surface_area(cubes)

print(len(surface_area))

# We'll grow an area outside the cubes and count the cube surfaces it touches. First we need to get bounds for
# the cubes so we can pick something outside (and stop the region growing indefinitely

bounds = [(min(cube.centre[i] for cube in cubes), max(cube.centre[i] for cube in cubes)) for i in range(3)]

# We pick a cube around the edge.
steam_start = Cube(Point3D(bounds[0][1] + 1, bounds[1][1] + 1, bounds[2][1] + 1))

steam_cubes = set([steam_start])
lava_cubes = set(cubes)

exterior_faces = set()

# Firstly expand the frontier where we can
added = True
new_cubes = True
while new_cubes:
    new_cubes = set()
    for cube in steam_cubes:
        for neighbour in cube.neighbours():
            if neighbour in lava_cubes:
                continue

            if out_of_bounds(neighbour, bounds):
                continue
            if neighbour not in steam_cubes:
                new_cubes.add(neighbour)

    steam_cubes |= new_cubes
    # print(len(new_cubes), len(steam_cubes))

steam_surface_area = get_surface_area(steam_cubes)

exterior_surface_area = steam_surface_area & surface_area
print(len(exterior_surface_area))

# common = cube.faces_set & surface_area
# for face in cube.faces:
#    pass
