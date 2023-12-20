import sys
import math


class Pulse(type):
    def __repr__(cls):
        return cls.str


class LowPulse(metaclass=Pulse):
    value = True
    str = "-low->"


class HighPulse(metaclass=Pulse):
    value = False
    str = "->high->"


class Module:
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []

        self.reset()

    def reset(self):
        self.data_queue = []
        self.low_count = 0
        self.high_count = 0

    def connect_to(self, object):
        self.outputs.append(object)
        object.connect_from(self)

    def connect_from(self, other):
        self.inputs.append(other)

    def send(self, pulse, sender):
        if pulse is LowPulse:
            self.low_count += 1
        else:
            self.high_count += 1
        # print(f"{sender.name} {pulse} {self.name}")
        self.data_queue.append(pulse)

    def state(self):
        return None

    def __repr__(self):
        return f"{self.__class__.__name__}:{self.name}"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return False


class Output(Module):
    def operate(self):
        # Don't do anything
        if LowPulse in self.data_queue:
            print("howdy", button_pushes)
            raise jim
        self.data_queue = []
        return []


class Broadcaster(Module):
    def push(self):
        # We put a low-pulse on the input
        self.send(LowPulse, self)

    def operate(self):
        # All of our outputs get an input if one exists:
        if not self.data_queue:
            return []

        data = self.data_queue.pop(0)
        for output in self.outputs:
            output.send(data, self)

        return self.outputs


class FlipFlop(Module):
    def reset(self):
        super().reset()
        self.value = False

    def state(self):
        return self.value

    def operate(self):
        if not self.data_queue:
            return []

        data = self.data_queue.pop(0)

        if data is HighPulse:
            return []

        # It's a LowPulse so we flip!
        data = LowPulse if self.value else HighPulse
        self.value = not self.value

        for output in self.outputs:
            output.send(data, self)

        return self.outputs


class Conjunction(Module):
    def reset(self):
        super().reset()

        if hasattr(self, "last_inputs"):
            self.last_inputs = {name: LowPulse for name in self.last_inputs}
        else:
            self.last_inputs = {}

    def state(self):
        # This seems expensive
        return tuple(sorted(list(self.last_inputs.items())))

    def connect_from(self, other):
        super().connect_from(other)
        self.last_inputs[other.name] = LowPulse

    def send(self, data, sender):
        self.last_inputs[sender.name] = data

        super().send(data, sender)
        self.data_queue.append(data)

    def operate(self):
        if not self.data_queue:
            return []

        # We've already consumed this item
        self.data_queue.pop(0)

        data = LowPulse if all(pulse is HighPulse for pulse in self.last_inputs.values()) else HighPulse
        for output in self.outputs:
            output.send(data, self)

        return self.outputs


def all_state(objects):
    # Dicts maintain their insertion order and we don't modify the object list after the start, so this should be ok I think?
    return tuple(object.state() for object in objects.values())


with open(sys.argv[1], "r") as file:
    data = [line.strip().split(" -> ") for line in file]

types = {"b": Broadcaster, "%": FlipFlop, "&": Conjunction}
objects = {}

# Do a first pass to instantiate all the objects
for source, destinations in data:
    typef = source[0]
    name = source if typef in "bo" else source[1:]

    obj = types[typef](name)
    objects[obj.name] = obj


for source, destinations in data:
    destinations = [d.strip() for d in destinations.split(",")]
    typef = source[0]
    name = source if typef in "bo" else source[1:]
    for dest in destinations:
        try:
            target = objects[dest]
        except KeyError:
            target = Output(dest)
            objects[target.name] = target
        objects[name].connect_to(target)

broadcaster = objects["broadcaster"]
object_queue = []
button_pushes = 0

while True:
    broadcaster.push()

    object_queue.extend(broadcaster.operate())

    while object_queue:
        obj = object_queue.pop(0)
        object_queue.extend(obj.operate())

    button_pushes += 1
    if button_pushes == 1000:
        break


low_count = sum(object.low_count for object in objects.values())
high_count = sum(object.high_count for object in objects.values())

print(low_count * high_count)

# Now we go again, but watch for cycles in the output conjunction.
for object in objects.values():
    object.reset()

# First we have to find the output conjunction
outputs = [obj for obj in objects.values() if isinstance(obj, Output)]

assert len(outputs) == 1 and len(outputs[0].inputs) == 1

# We expect the output to have exactly one input, and it should be a conjunction
output_node = outputs[0].inputs[0]

assert isinstance(output_node, Conjunction)

# We now want to look for cycles in the outputs of this nodes inputs. We can then find the point at which they're all going to output high


orig_outputs = list(broadcaster.outputs)

cycles = []

for orig_output in orig_outputs:
    for object in objects.values():
        object.reset()

    button_pushes = 0
    object_queue = []
    button_pushes = 0
    states = {all_state(objects): button_pushes}

    broadcaster.outputs = [orig_output]
    while True:
        broadcaster.push()
        button_pushes += 1

        object_queue.extend(broadcaster.operate())

        while object_queue:
            obj = object_queue.pop(0)
            object_queue.extend(obj.operate())

        state = all_state(objects)

        if state in states:
            cycle_length = button_pushes - states[state]
            run_up = states[state]
            print(f"Cycled back to state {states[state]} after {button_pushes} button_pushes {cycle_length=}")
            cycles.append(cycle_length)
            break

        states[state] = button_pushes

print(math.lcm(*cycles))
