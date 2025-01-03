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
queue = {i: [] for i in range(len(nodes))}
done = False
nat_pack = None
read_nothing = {}
last = None
done_part_one = False

while not done:
    waiting = []

    for i, node in enumerate(nodes):
        try:
            node.resume()
        except intcode.InputStall:
            assert len(node.output) == 0
            waiting.append(i)
        except intcode.OutputStall:
            assert len(node.output) == 3
            target = node.output[0]
            if target == 255:
                if not done_part_one:
                    print(node.output[2])
                    done_part_one = True
                nat_pack = node.output[1:]
                node.output = []
                continue
            queue[target].extend(node.output[1:])
            node.output = []

    if (
        len(read_nothing) == len(nodes)
        and all(read_nothing.values())
        and 0 == sum(len(q) for q in queue.values())
        and nat_pack
    ):
        if nat_pack[1] == last:
            print(last)
            break
        last = nat_pack[1]
        queue[0].extend(nat_pack)

    for node in waiting:
        l = queue[node]
        value = -1
        have_nothing = True
        if l:
            value = l.pop(0)
            have_nothing = False
        read_nothing[node] = have_nothing
        nodes[node].inputs.append(value)
