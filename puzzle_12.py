import sys
import copy


def is_small(node):
    return node.islower()


class Path:
    def __init__(self, graph, path=[]):
        self.small_visited = set([node for node in path if is_small(node)])
        self.path = path
        self.graph = graph

    def add_node(self, node):
        new = copy.deepcopy(self)
        new.path += [node]

        if is_small(node):
            new.small_visited.add(node)
        return new

    def can_visit(self, node):
        if not is_small(node):
            return True

        return node not in self.small_visited


class RevisitPath(Path):
    def __init__(self, graph, path=[]):
        super().__init__(graph, path)
        self.small_double_visit = None

    def add_node(self, node):
        double = is_small(node) and node in self.small_visited

        new = super().add_node(node)
        if double:
            if new.small_double_visit:
                assert False
            else:
                new.small_double_visit = node
        return new

    def can_visit(self, node):
        if super().can_visit(node):
            return True

        # We're only allowed to revisit a small one once
        if self.small_double_visit is not None:
            return False

        return node not in ["start", "end"]


class Graph:
    def __init__(self, filename, path_class):
        self.nodes = {}
        self.path_class = path_class

        with open(sys.argv[1], "r") as file:
            for line in file:
                a, b = line.strip().split("-")
                try:
                    self.nodes[a].add(b)
                except KeyError:
                    self.nodes[a] = set([b])
                try:
                    self.nodes[b].add(a)
                except KeyError:
                    self.nodes[b] = set([a])

    def walk(self, node, path):
        try:
            for neighbour in self.nodes[node]:
                if neighbour == "end":
                    yield path.path + ["end"]
                    continue
                if not path.can_visit(neighbour):
                    continue
                for full_path in self.walk(neighbour, path.add_node(neighbour)):
                    yield full_path
        except KeyError:
            pass

    def get_paths(self):

        path = self.path_class(self, ["start"])

        for full_path in self.walk("start", path):
            yield full_path


graph = Graph(sys.argv[1], Path)

count = 0
for path in graph.get_paths():
    # print(path)
    count += 1

print(count)

graph = Graph(sys.argv[1], RevisitPath)

count = 0
for path in graph.get_paths():
    # print(path)
    count += 1

print(count)
