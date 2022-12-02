import sys
import copy


class Path:
    def __init__(self, graph, path, small_visited):
        self.path = path
        self.graph = graph
        self.small_visited = set(small_visited)

    def add_node(self, node):
        new = type(self)(self.graph, self.path + [node], self.small_visited)

        if node in self.graph.small:
            new.small_visited.add(node)
        return new

    def can_visit(self, node):
        if node not in self.graph.small:
            return True

        return node not in self.small_visited


class RevisitPath(Path):
    def __init__(self, graph, path, small_visited):
        super().__init__(graph, path, small_visited)
        self.small_double_visit = None

    def add_node(self, node):
        double = node in self.graph.small and node in self.small_visited
        new = super().add_node(node)
        new.small_double_visit = self.small_double_visit
        if double and not new.small_double_visit:
            new.small_double_visit = node
        return new

    def can_visit(self, node):
        if super().can_visit(node):
            return True

        # We're only allowed to revisit a small one once
        if self.small_double_visit is not None:
            return False

        return node not in graph.ends


class Graph:
    def __init__(self, filename, path_class):
        self.nodes = {}
        self.path_class = path_class
        self.small = set()
        self.ends = {"start", "end"}

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
                for node in (a, b):
                    if node.islower():
                        self.small.add(node)

    def walk(self, node, path):
        try:
            for neighbour in self.nodes[node]:
                if neighbour == "end":
                    yield path.path
                    continue
                if not path.can_visit(neighbour):
                    continue
                for full_path in self.walk(neighbour, path.add_node(neighbour)):
                    yield full_path
        except KeyError:
            pass

    def get_paths(self):

        path = self.path_class(self, ["start"], ["start"])

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
