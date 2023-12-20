import sys


class Packet:
    def __init__(self, version, type_id, stream):
        self.version = version
        self.type_id = type_id
        self.length = 6
        self.packets = []

    def print_lines(self):
        yield f"[PACKET:{self.__class__.__name__}] version={self.version} type_id={self.type_id} value={self.value}"

    def __repr__(self):
        return "\n".join(self.print_lines())

    def version_sum(self):
        total = self.version

        for packet in self.packets:
            total += packet.version_sum()

        return total


class Literal(Packet):
    type_id = 4

    def __init__(self, version, type_id, stream):
        super().__init__(version, type_id, stream)
        self.value = 0
        more = 1
        pos = 0
        while more:
            val = int(stream[pos : pos + 5], 2)
            pos += 5
            more = val >> 4
            self.value <<= 4
            self.value |= val & 0xF
        self.length += pos


class Operator(Packet):
    type_id = 0

    def __init__(self, version, type_id, stream):
        super().__init__(version, type_id, stream)
        self.packets = []

        self.operator_type = int(stream[0], 2)
        if self.operator_type:
            self.length += 11 + 1
            self.num_packets = int(stream[1:12], 2)
            self.parse_packets(stream[12:])
        else:
            self.length += 15 + 1
            self.sub_length = int(stream[1:16], 2)
            self.parse_bits(stream[16:])

    def parse_packets(self, stream):
        while len(self.packets) < self.num_packets:
            packet, stream = packet_factory(stream)
            self.packets.append(packet)
            self.length += packet.length

    def parse_bits(self, stream):
        consumed = 0
        while consumed < self.sub_length:
            packet, stream = packet_factory(stream)
            self.packets.append(packet)
            consumed += packet.length
            self.length += packet.length

    def print_lines(self):
        for line in super().print_lines():
            yield line
            for packet in self.packets:
                for line in packet.print_lines():
                    yield "  " + line

    @property
    def value(self):
        raise ValueError("Base operator doesn't implement value")


class Sum(Operator):
    type_id = 0

    @property
    def value(self):
        return sum(packet.value for packet in self.packets)


class Product(Operator):
    type_id = 1

    @property
    def value(self):
        total = 1
        for packet in self.packets:
            total *= packet.value
        return total


class Minimum(Operator):
    type_id = 2

    @property
    def value(self):
        return min((packet.value for packet in self.packets))


class Maximum(Operator):
    type_id = 3

    @property
    def value(self):
        return max((packet.value for packet in self.packets))


class GreaterThan(Operator):
    type_id = 5

    @property
    def value(self):
        a, b = self.packets

        return 1 if a.value > b.value else 0


class LessThan(Operator):
    type_id = 6

    @property
    def value(self):
        a, b = self.packets

        return 1 if a.value < b.value else 0


class Equal(Operator):
    type_id = 7

    @property
    def value(self):
        a, b = self.packets

        return 1 if a.value == b.value else 0


packet_classes = [Literal, Sum, Product, Minimum, Maximum, GreaterThan, LessThan, Equal]
packet_machines = {packet.type_id: packet for packet in packet_classes}


def packet_factory(stream):
    if len(stream) <= 6 or "1" not in stream:
        # we're done
        return None, ""

    version, type_id = int(stream[:3], 2), int(stream[3:6], 2)
    try:
        packet_type = packet_machines[type_id]
    except KeyError:
        packet_type = Operator
    packet = packet_type(version, type_id, stream[6:])

    return packet, stream[packet.length :]


# Start by grabbing the hex and binarifying it

with open(sys.argv[1], "r") as file:
    hexa_str = file.read().strip()
    hexa = int(hexa_str, 16)
    # it needs 0 padding to the right width
    width = len(hexa_str) * 4
    stream = f"{hexa:b}"
    padding = width - len(stream)
    stream = ("0" * padding) + stream


total = 0
outermost_value = None
while len(stream) >= 6 or "1" in stream:
    packet, stream = packet_factory(stream)
    if packet is None:
        break
    print(packet)
    total += packet.version_sum()

    if outermost_value is None:
        outermost_value = packet.value

print(total)

# For part 2 we want the value of the outermost packet
print(outermost_value)
