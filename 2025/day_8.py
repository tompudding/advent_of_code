import sys
from utils import Point3D as Point, prod


class Circuit:
    def __init__(self, a, b):
        self.points = {a, b}

    def add(self, a):
        self.points.add(a)


def scan_for_data(max_to_scan, distance_list):

    circuits = {}
    last_added = None

    for (a, b), distance in distance_list[:max_to_scan]:
        circuit_a = circuits.get(a, None)
        circuit_b = circuits.get(b, None)

        if circuit_a and circuit_a is circuit_b:
            # These are both already accounted for
            pass
        elif circuit_a and circuit_b is None:
            circuit_a.add(b)
            circuits[b] = circuit_a
        elif circuit_b and circuit_a is None:
            circuit_b.add(a)
            circuits[a] = circuit_b
        elif circuit_a and circuit_b:
            # We need to merge all these
            for point in circuit_b.points:
                circuit_a.add(point)
                circuits[point] = circuit_a

        elif circuit_a is None and circuit_b is None:
            circuit = Circuit(a, b)
            circuits[a] = circuits[b] = circuit

        if len(set(circuits.values())) == 1 and len(list(circuits.values())[0].points) == len(points):
            last_added = (a, b)
            break
    return circuits, last_added


with open(sys.argv[1]) as file:
    points = [Point(*(int(v) for v in line.strip().split(","))).to_int() for line in file]

distances = {}

for i in range(len(points)):
    for j in range(i + 1, len(points)):
        distances[points[i], points[j]] = (points[i] - points[j]).length()


distance_list = list(distances.items())
distance_list.sort(key=lambda x: x[1])

circuits, ignore = scan_for_data(10 if len(points) < 50 else 1000, distance_list)

unique_circuits = list(set(circuits.values()))
unique_circuits.sort(key=lambda x: len(x.points), reverse=True)

print(prod(len(circuit.points) for circuit in unique_circuits[:3]))

ignore, last_added = scan_for_data(len(distance_list), distance_list)
print(last_added[0].x * last_added[1].x)
