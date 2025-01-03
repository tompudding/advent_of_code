import sys
import intcode
import os
import collections

with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

nodes = [intcode.IntCode(instructions, [i], max_out=3) for i in range(50)]


time = 0
queue = collections.defaultdict(list)
done = False

while not done:
    waiting = []

    for i, node in enumerate(nodes):
        try:
            node.step(1)
        except intcode.InputStall:
            assert len(node.output) == 0
            waiting.append(i)
        except intcode.OutputStall:
            assert len(node.output) == 3
            target = node.output[0]
            if target == 255:
                done = True
                print(node.output[2])
                break
            queue[target].extend(node.output[1:])
            node.output = []

    for node in waiting:
        l = queue[node]
        value = -1
        if l:
            value = l.pop(0)
        nodes[node].inputs.append(value)
