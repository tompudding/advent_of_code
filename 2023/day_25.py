import sys
import networkx

connections = {}

links = []
nodes = set()

with open(sys.argv[1], "r") as file:
    for line in file:
        start, ends = line.strip().split(":")
        ends = [part.strip() for part in ends.split()]
        nodes.add(start)
        nodes |= set(ends)

        for end in ends:
            links.append((start, end))

print(len(links))

graph = networkx.Graph()

for node in nodes:
    graph.add_node(node)

for start, end in links:
    graph.add_edge(start, end, capacity=1)

p = networkx.periphery(graph)
x = networkx.single_source_shortest_path_length(graph, p[0])
a = p[0]
b = list(x)[-1]
cut_value, partition = networkx.minimum_cut(graph, a, b)
print(cut_value, partition)
a, b = partition
print(len(a) * len(b))
