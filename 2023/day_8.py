import sys
import math
from functools import reduce


class Node:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    def step(self, direction):
        return {"L": self.left, "R": self.right}[direction]


nodes = {}
first_node = None

with open(sys.argv[1], "r") as file:
    lines = file.readlines()

    path = lines[0].strip()

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        node, points = line.split("=")
        node_name = node.strip()
        points = (part.strip() for part in points.strip().strip("()").split(","))

        node = Node(node_name, *points)
        nodes[node_name] = node

        if not first_node:
            first_node = node

for node in nodes.values():
    node.left = nodes[node.left]
    node.right = nodes[node.right]

node = nodes["AAA"]
visited = set()
steps = 0

while node.name != "ZZZ":
    path_pos = steps % len(path)
    node = node.step(path[path_pos])
    steps += 1

print(steps)

cycles = []
run_ups = []

for start_node in nodes.values():
    if start_node.name[-1] != "A":
        continue

    node = start_node
    steps = 0
    visited = {(node.name, 0): 0}
    z_nodes = []

    while True:
        path_pos = steps % len(path)

        node = node.step(path[path_pos])
        steps += 1

        path_pos = steps % len(path)

        key = (node.name, path_pos)

        try:
            visited[key] += 1
            # At 3 we've done two complete cycles, so we can see how long the run-up was
            if visited[key] == 3:
                assert len(z_nodes) == 2
                cycle_length = z_nodes[1] - z_nodes[0]
                run_up = z_nodes[0] - cycle_length
                if run_up != 0:
                    raise Exception("This is more complex")
                cycles.append(cycle_length)
                run_ups.append(run_up)
                break
        except KeyError:
            visited[key] = 1

        if node.name.endswith("Z"):
            z_nodes.append(steps)

print(math.lcm(*cycles))
