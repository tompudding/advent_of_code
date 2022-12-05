import sys
import re

class Move:
    def __init__(self, num, src, dst):
        self.num = int(num)
        self.src = int(src)-1
        self.dst = int(dst)-1

def parse_move(line):
    return Move(*re.match('move (\d+) from (\d+) to (\d+)',line).groups())

setup_lines = []
moves = []

with open(sys.argv[1], 'r') as file:
    for line in file:
        if '[' in line:
            setup_lines.append(line.strip('\n'))
            num_stacks = line.count(']')
        elif line.startswith('move'):
            moves.append(parse_move(line.strip()))

stacks = [[] for i in range(num_stacks)]

for line in setup_lines[::-1]:
    for stack in range(num_stacks):
        pos = 1+(stack *4)
        if line[pos].strip():
            stacks[stack].append(line[pos])

orig_stacks = [[crate for crate in stack] for stack in stacks]
for move in moves:
    for i in range(move.num):
        item = stacks[move.src].pop()
        stacks[move.dst].append(item)

print(''.join(stack[-1] for stack in stacks))

#Part 2

stacks = orig_stacks
for move in moves:
    items = stacks[move.src][-move.num:]
    stacks[move.src] = stacks[move.src][:-move.num]
    stacks[move.dst].extend(items)

print(''.join(stack[-1] for stack in stacks))


