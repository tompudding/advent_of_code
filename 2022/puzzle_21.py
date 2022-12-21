import sys


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a // b


op_map = {"+": add, "-": sub, "*": mul, "/": div}


class Node:
    def __init__(self, name, operands=[], value=None, op=None):
        self.name = name
        self.operands = operands
        self.op = op
        self.value = value
        self.used_by = []

    def resolve(self):
        if all(operand.value is not None for operand in self.operands):
            self.value = self.op(self.operands[0].value, self.operands[1].value)
            return True
        return False


nodes = {}
value_nodes = {}

with open(sys.argv[1], "r") as file:
    for line in file:
        line = line.strip()
        name, rest = line.split(": ")
        try:
            value = int(rest)
            node = Node(name, value=value)
            nodes[node.name] = node
            continue
        except ValueError:
            pass
        parts = [part.strip() for part in rest.split()]
        node = Node(name, operands=[parts[0], parts[2]], op=op_map[parts[1]])
        nodes[node.name] = node

waiting = set()
live = set()
dead = set()

# Do a pass filling in references
for name, node in nodes.items():
    node.operands = [nodes[operand] for operand in node.operands]

    for operand in node.operands:
        operand.used_by.append(node)

for name, node in nodes.items():

    if node.value is not None:
        if node.used_by:
            live.add(node)
        else:
            done.add(node)
    else:
        waiting.add(node)

while waiting:
    new_live = set()

    for node in live:
        all_resolved = True
        for parent in node.used_by:
            if parent in waiting and parent.resolve():
                waiting.remove(parent)
                new_live.add(parent)
            else:
                all_resolved = False
        if all_resolved:
            dead.add(node)
        else:
            new_live.add(node)
    live = new_live

print(nodes["root"].value)
