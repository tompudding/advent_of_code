import sys
import copy


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a // b


def equal(a, b):
    print(f"equal: {a=}, {b=}")
    return a == b


op_map = {"+": add, "-": sub, "*": mul, "/": div, "==": equal}
op_str = {op: op_name for op_name, op in op_map.items()}
inverse = {add: sub, sub: add, mul: div, div: mul}


class Expression:
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        if self.op:
            return f"({self.lhs} {op_str[self.op]} {self.rhs})"
        else:
            return self.lhs


class Node:
    def __init__(self, name, operands=[], value=None, op=None):
        self.name = name
        self.operands = operands
        self.op = op
        self.value = value
        self.used_by = []
        self.expression = False

    def resolve(self):
        if all(operand.value is not None for operand in self.operands):
            self.value = self.op(self.operands[0].value, self.operands[1].value)
            return True

        # We can still do it if exactly one is an expression, including us
        if self.expression:
            return True

        if self.operands[0].expression and self.operands[1].value is not None:
            self.expression = Expression(self.op, self.operands[0].expression, self.operands[1].value)
            return True
        elif self.operands[1].expression and self.operands[0].value is not None:
            self.expression = Expression(self.op, self.operands[0].value, self.operands[1].expression)
            return True

        return False


def solve(nodes):
    waiting = set()
    live = set()
    dead = set()

    for name, node in nodes.items():
        if node.value is not None or node.expression:
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

    return nodes["root"]


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


# Do a pass filling in references
for name, node in nodes.items():
    node.operands = [nodes[operand] for operand in node.operands]

    for operand in node.operands:
        operand.used_by.append(node)

orig_nodes = copy.deepcopy(nodes)

root = solve(nodes)
print(root.value)

nodes = orig_nodes

# For part 2 things are much more complicated
nodes["root"].op = equal
nodes["root"].value = None

nodes["humn"].value = None
nodes["humn"].expression = Expression(None, "humn", None)

root = solve(nodes)

lhs = None
accumulator = 0
expression = root.expression
while expression.op:
    op, lhs, rhs = expression.op, expression.lhs, expression.rhs
    print(f"{expression} == {accumulator}")
    if op == equal:
        accumulator = rhs
        expression = lhs
        continue

    # One of the lhs or rhs should be an integer
    if isinstance(lhs, Expression):
        # f(humn) op k1 = k2 => f(humn) = k2 op_inv k1
        accumulator = inverse[op](accumulator, rhs)
        expression = lhs
    elif isinstance(rhs, Expression):
        # k1 op f(humn) = k2 => k1 = k2 op_inv f(humn) => k1-k2 = op_inv(f f(humn)) = k2 op_inv k1
        if op in (add, mul):
            accumulator = inverse[op](accumulator, lhs)
            expression = rhs
        else:
            # The non-associative ones are slightly different
            accumulator = op(lhs, accumulator)
            expression = rhs


print(accumulator)
