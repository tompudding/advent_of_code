import sys
import intcode
import os
import time
import heapq
import collections

def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

program = intcode.IntCode(instructions, [])

#program.debugger()

def get_state(program):
    return program.program[1030:1050]

def set_state(program, state):
    program.program[1030:1050] = state

def get_neighbours(pos):

    for direction in range(1, 5):
        set_state(program, states[pos])
        program.inputs.append(direction)

        try:
            program.resume()
        except intcode.InputStall:
            assert len(program.output) == 1
            output = program.output.pop()
            new_pos = tuple(program.program[1039:1041])
            if output == 0:
                walls.add(new_pos)
                continue
            if output == 2:
                assert new_pos == (33, 35)

            states[new_pos] = get_state(program)
            yield direction, new_pos



frontier = []
start = (21, 21)
end = (33, 35)

heapq.heappush(frontier, (0, start))
came_from = {}
cost_so_far = {}
came_from[start] = None
cost_so_far[start] = 0
states = {start : get_state(program)}
walls = set()

while frontier:
    s, current = heapq.heappop(frontier)

    for direction, next_pos in get_neighbours(current):
        new_cost = cost_so_far[current] + 1
        if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
            cost_so_far[next_pos] = new_cost
            priority = new_cost + heuristic(end, next_pos)
            heapq.heappush(frontier, (priority, next_pos))
            came_from[next_pos] = current

current = end

path = []
cost = 0
while current != start:
    cost += 1
    path.append(current)
    current = came_from[current]
path.append(start)
path.reverse()
print(path)
print('COST:',cost)

# For part 2 we want to explore every possible neighbour.

frontier = collections.deque()
frontier.append(start)
reached = set()
reached.add(start)


while frontier:
    current = frontier.popleft()
    for direction, next_pos in get_neighbours(current):
        if next_pos not in reached:
            frontier.append(next_pos)
            reached.add(next_pos)

# Now we have every position and every wall, we can expand the oxygen:

time = 0
oxygen = {end}

while True:
    new_oxygen = set()
    for source in oxygen:
        for direction in (0, 1), (0, -1), (1, 0), (-1, 0):
            new_pos = (source[0] + direction[0], source[1] + direction[1])
            if new_pos in walls:
                continue
            new_oxygen.add(new_pos)
    oxygen |= new_oxygen
    time += 1
    if len(oxygen) == len(reached):
        break

print(time)
