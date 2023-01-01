import sys


class Body:
    def __init__(self, name):
        self.name = name
        self.satellites = []
        self.count = 0
        self.orbiting = None

    def add_orbit(self, other):
        self.satellites.append(other)
        other.orbiting = self

    def get_chain(self):
        node = self.orbiting
        chain = []
        while node:
            chain.append(node)
            node = node.orbiting

        return chain

    def __repr__(self):
        return f"<{self.name}>"


bodies = {}


def get_body(name):
    try:
        return bodies[name]
    except KeyError:
        body = Body(name)
        bodies[name] = body
        return body


def count_orbits(count, body):

    body.count = count

    for moon in body.satellites:
        count_orbits(count + 1, moon)


with open(sys.argv[1], "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        centre, satellite = (get_body(name) for name in line.split(")"))

        centre.add_orbit(satellite)

count_orbits(0, bodies["COM"])

print(sum(body.count for body in bodies.values()))

my_chain = bodies["YOU"].get_chain()
target_chain = bodies["SAN"].get_chain()

target_set = {body.name: pos for pos, body in enumerate(target_chain)}

final_path = []

for body in my_chain:
    if body.name not in target_set:
        final_path.append(body)
        continue
    # The body is in it, so we can go from there
    final_path.extend(target_chain[: target_set[body.name] + 1][::-1])
    break

print(len(final_path) - 1)
