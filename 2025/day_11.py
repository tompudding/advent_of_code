import sys
import copy
import collections
import utils


class Node:
    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.name] = node

    def topological_sort(self):
        # Let's use Kahn's algorithm, I found it on Wikipedia
        all_destinations = set()
        for node in self.nodes.values():
            all_destinations |= node.neighbours

        temp = copy.deepcopy(self.nodes)
        incoming = collections.defaultdict(set)
        for node in temp.values():
            for neighbour in node.neighbours:
                incoming[neighbour].add(node.name)

        start_nodes = self.nodes.keys() - all_destinations
        self.top_sorted = []
        while start_nodes:
            s = temp[start_nodes.pop()]
            self.top_sorted.append(s.name)
            for m in s.neighbours:
                incoming[m].remove(s.name)

                if len(incoming[m]) == 0:
                    start_nodes.add(m)

    def count_paths(self, start, end):
        num_paths = {name: 0 for name in self.nodes}
        num_paths[start] = 1

        for node in self.top_sorted:
            for neighbour in graph.nodes[node].neighbours:
                num_paths[neighbour] += num_paths[node]
        return num_paths[end]


graph = Graph()

with open(sys.argv[1]) as file:
    for line in file:
        name, rest = line.strip().split(": ")
        neighbours = {part.strip() for part in rest.split()}
        graph.add_node(Node(name, neighbours))

graph.add_node(Node("out", set()))
graph.topological_sort()

print(graph.count_paths("you", "out"))


print(
    utils.prod(
        graph.count_paths(start, end) for (start, end) in (("svr", "fft"), ("fft", "dac"), (("dac", "out")))
    )
)
