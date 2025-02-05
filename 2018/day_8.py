import sys


class Node:
    def __init__(self, numbers, pos, level):
        num_children = numbers[pos]
        num_metadata = numbers[pos + 1]
        self.level = level
        self.children = []
        pos += 2
        for i in range(num_children):
            child = Node(numbers, pos, level + 1)
            pos = child.pos
            self.children.append(child)
        self.metadata = numbers[pos : pos + num_metadata]
        self.pos = pos + num_metadata

    def metadata_total(self):
        return sum(self.metadata) + sum(child.metadata_total() for child in self.children)

    def value(self):
        if len(self.children) == 0:
            return sum(self.metadata)

        total = 0
        for val in self.metadata:
            if val == 0:
                # what does this mean?
                continue
            try:
                total += self.children[val - 1].value()
            except IndexError:
                continue
        return total

    def __repr__(self):
        spacer = " " * self.level
        out = [f"{spacer}Node with {len(self.children)} children and metadata={self.metadata}:"]
        for i, child in enumerate(self.children):
            out.append(f"{spacer}{i} : {child}")
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    numbers = [int(v) for v in file.read().strip().split()]

tree = Node(numbers, 0, 0)
# print(tree)
print(tree.metadata_total())
print(tree.value())
