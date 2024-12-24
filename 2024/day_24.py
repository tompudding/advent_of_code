import sys
from dataclasses import dataclass


@dataclass
class Value:
    name: str
    state: int

    def value(self):
        return self.state


@dataclass
class Gate:
    a: str
    b: str
    result: str

    def value(self):
        return self.op(gates[self.a].value(), gates[self.b].value())


class And(Gate):
    name = "AND"

    def op(self, a, b):
        return a & b


class Xor(Gate):
    name = "XOR"

    def op(self, a, b):
        return a ^ b


class Or(Gate):
    name = "OR"

    def op(self, a, b):
        return a | b


gate_map = {gate.name: gate for gate in (And, Xor, Or)}
gates = {}

with open(sys.argv[1], "r") as file:
    value_lines, gate_lines = file.read().split("\n\n")

for line in value_lines.splitlines():
    name, val = line.strip().split(": ")
    val = Value(name, int(val))
    gates[name] = val

for line in gate_lines.splitlines():
    rest, result = line.strip().split(" -> ")
    a, op, b = rest.split()
    assert result not in gates
    gates[result] = gate_map[op](a, b, result)

for i in range(32):
    if f"z{i:02d}" in gates:
        num_bits = i + 1

total = 0
i = 0
while True:
    try:
        total |= gates[f"z{i:02d}"].value() << i
        i += 1
    except KeyError:
        break

print(total)
