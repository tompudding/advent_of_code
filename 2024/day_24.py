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

    def __init__(self, a, b, result):
        self.a = a
        self.b = b
        self.result = result

        self.reg_names = ["", ""]
        self.bits = [None, None]

        for x, pos in ((a, 0), (b, 1)):
            try:
                num = int(x[1:])
                reg = x[0]
                self.reg_names[pos] = reg
                self.bits[pos] = num
            except ValueError:
                pass

    def set_a(self, name):
        self.a = name
        try:
            self.bits[0] = int(name[-2:])
        except ValueError:
            pass

    def set_b(self, name):
        self.b = name
        try:
            self.bits[1] = int(name[-2:])
        except ValueError:
            pass

    def set_result(self, name):
        self.result = name

    def value(self):
        return self.op(gates[self.a].value(), gates[self.b].value())

    def __repr__(self):
        return f"{self.a} {self.name} {self.b} -> {self.result}"


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

num_bits = 46


def get_bit(i):
    return gates[f"z{i:02d}"].value()


def calculate_z(num_bits):
    total = 0
    for i in range(num_bits):
        try:
            total |= get_bit(i) << i
        except KeyError:
            break
    return total


swaps = []


def swap(a, b):
    gates[a], gates[b] = gates[b], gates[a]
    gates[a].result = a
    gates[b].result = b
    swaps.extend([a, b])


# These were obtained by iteratively running the relabeling process until the first bit that looked wrong.
# TODO: Do that programatically
swap("shh", "z21")
swap("vgs", "dtk")
swap("dqr", "z33")
swap("pfw", "z39")

print(",".join(sorted(swaps)))


def relabel(label_from, label_to):
    if label_from == label_to or label_from.startswith("z") and label_from[1:].isnumeric():
        return False
    print("relabel", label_from, label_to)
    for gate in gates.values():
        if isinstance(gate, Value):
            continue
        if gate.result == label_from:
            gate.set_result(label_to)
        if gate.a == label_from:
            gate.set_a(label_to)
        if gate.b == label_from:
            gate.set_b(label_to)

    x = gates[label_from]
    del gates[label_from]
    gates[label_to] = x
    return True


# Do a bit of relabling
changed = True
while changed:
    changed = False
    for result, gate in gates.items():
        if isinstance(gate, Value):
            continue
        if gate.reg_names[0] and gate.reg_names[1] and gate.bits[0] == gate.bits[1]:
            if gate.name == "XOR":
                changed = relabel(gate.result, f"ADD{gate.bits[0]:02d}")
                if changed:
                    break
            elif gate.name == "AND":
                changed = relabel(gate.result, f"CARRYA{gate.bits[0]:02d}")
                if changed:
                    break
            else:
                print(gate)
                raise jim
        if gate.name == "OR":
            if gate.a.startswith("CARRYA"):
                changed = relabel(gate.b, f"CARRYB{gate.bits[0]:02d}")
            elif gate.b.startswith("CARRYA"):
                changed = relabel(gate.a, f"CARRYB{gate.bits[1]:02d}")
            else:
                continue

            changed |= relabel(gate.result, f"CARRYC{gate.bits[0]:02d}")
            if changed:
                break


for result, gate in gates.items():
    print(gate)

num_bits = 46
print(calculate_z(num_bits))

X = 0
Y = 0


@dataclass
class XVal:
    bit: int

    def value(self):
        return (X >> self.bit) & 1


@dataclass
class YVal:
    bit: int

    def value(self):
        return (Y >> self.bit) & 1


# For part 2 we can use dynamic gates that can simulate any value
for i in range(num_bits - 1):
    gates[f"x{i:02d}"] = XVal(i)
    gates[f"y{i:02d}"] = YVal(i)

# Now for each bit we'll test adding 0+0, 0+1, 1+0, 1+1 to make sure all the gates for that bit are set up
# correctly (and the carry for the next bit)


for bit in range(num_bits - 1):

    X = 0 << bit
    Y = 0 << bit

    if get_bit(bit) != 0:
        print("bad zero at", bit)
        break

    if get_bit(bit + 1) != 0:
        print("bad carry at", bit)
        break

    X = 1 << bit
    Y = 0 << bit

    if get_bit(bit) != 1:
        print("bad one at", bit)
        break

    if get_bit(bit + 1) != 0:
        print("bad carry at", bit)
        break

    Y = 1 << bit

    if get_bit(bit) != 0:
        print("bad b", bit)
        break

    if get_bit(bit + 1) != 1:
        print("ffl", bit)
        break

    X = 0

    if get_bit(bit) != 1:
        print("bad one at", bit)
        break

    if get_bit(bit + 1) != 0:
        print("bad carry at", bit)
        break
