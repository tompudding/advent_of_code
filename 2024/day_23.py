import sys
import itertools
from collections import defaultdict

with open(sys.argv[1], "r") as file:
    all_pairs = [line.strip().split("-") for line in file]

connects = defaultdict(set)
edges = set()
nodes = {a for a, b in all_pairs} | {b for a, b in all_pairs}

for a, b in all_pairs:
    connects[a].add(b)
    connects[b].add(a)
    edges.add(tuple(sorted((a, b))))


def is_complete(graph, extra):
    return all(tuple(sorted((extra, item))) in edges for item in graph)


triples = set()

for machine, others in connects.items():
    # It's a tripair if there are two in the list of connected machines where both this machine and the other
    # are in each of their connecteds list

    for a, b in itertools.combinations(others, 2):
        if {machine, a}.issubset(connects[b]) and {machine, b}.issubset(connects[a]):
            triples.add(frozenset((a, b, machine)))


print(len([trip for trip in triples if any(t.startswith("t") for t in trip)]))

complete_graphs = {frozenset((a, b)) for (a, b) in edges}

for a, b in edges:
    new_graphs = set()
    for graph in complete_graphs:
        if a in graph and is_complete(graph, b):
            new_graphs.add(frozenset(graph | {b}))
        elif b in graph and is_complete(graph, a):
            new_graphs.add(frozenset(graph | {a}))
        else:
            new_graphs.add(graph)
    complete_graphs = new_graphs

complete_graphs = list(complete_graphs)
complete_graphs.sort(key=lambda x: len(x))
print(",".join(sorted(complete_graphs[-1])))
