import sys
import re
import heapq

names = []
valves = []
names_to_index = {}

class Valve:
    def __init__(self, index, flow_rate, neighbours, score=0):
        self.index = index
        self.name = names[index]
        self.flow_rate = flow_rate
        self.neighbour_names = neighbours
        self.score = score
        self.bit = (1 << self.index) if score != 0 else 0

    def set_neighbour_indices(self):
        self.neighbours = [(names_to_index[name], 1) for name in self.neighbour_names]

    def __repr__(self):
        return f'Valve {self.name} has flow rate={self.flow_rate}; tunnels lead to valves {self.neighbours}'

with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()
        if not (match := re.match('Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ', line)):
            print('skonk',line)
            continue
        name, flow_rate = match.groups()
        flow_rate = int(flow_rate)

        index = len(names)
        names.append(name)
        names_to_index[name] = index

        neighbours = [v.strip() for v in line.split('to valve')[1].strip('s ').split(',')]

        if flow_rate != 0:
            fake_name = f'{name}_on'
            current_neighbours = neighbours + [fake_name]
            names.append(fake_name)
            fake_index = index + 1
            names_to_index[fake_name] = fake_index
        else:
            current_neighbours = neighbours

        new_valve = Valve(index, flow_rate, current_neighbours)
        valves.append(new_valve)

        if flow_rate != 0:
            fake_valve = Valve(fake_index, 0, neighbours, score=flow_rate)
            valves.append(fake_valve)

        # We'all add another fake node for each node with a non-zero flow rate, that represents having turned on the valve at that point


#Once they've all been updated we can set the neighbours
for valve in valves:
    valve.set_neighbour_indices()

# Now we can collapse that graph by building a new one with

start = (names_to_index['AA'],0,0)
frontier = []
heapq.heappush(frontier, (0, start))
came_from = {start : None}

score_so_far = {start : 0}

max_length = 30

while frontier:
    s, node = heapq.heappop(frontier)
    current, length, turned_on = node
    current_valve = valves[current]
    score = score_so_far[(current, length, turned_on)]

    for next_index, distance in current_valve.neighbours:
        next_valve = valves[next_index]
        if next_valve.bit & turned_on:
            # We can't turn on the same thing twice
            continue

        new_length = length + distance
        if new_length >= max_length:
            continue

        new_node = (next_index, length + distance, turned_on | next_valve.bit)
        new_score = score + ((max_length - (length+distance)) * next_valve.score)

        #print(names[current], names[next_index], new_score)

        if new_node  not in score_so_far or new_score > score_so_far[new_node]:
            score_so_far[new_node] = new_score
            priority = -new_score

            heapq.heappush(frontier, (priority, new_node))
            came_from[new_node] = node

#Now we want to find the path with the largest score...
best = 0
bext_node = None
best_len = max_length
for node, score in score_so_far.items():
    (index, length, turned_on) = node
    #print(index, length, '%x' % turned_on, score)

    if score > best or (score == best and length < best_len):
        best = score
        best_node = node
        best_len = length

print(best)
print(best_node)

current = best_node

path = []
minute = 0
while current != start:
    index, length, turned_on = current
    path.append((index, names[index]))
    print(names[index], length, '%x' % turned_on)
    current = came_from[current]
path.append((0, names[0]))
path.reverse()
print(path)

pressure = 0
score = 0
for i, (index, name) in enumerate(path):
    valve = valves[index]
    score += valve.score * (max_length - i)
    if 0 == valve.score:
        print(name)
    else:
        print(f'{name} releases {valve.score} * {max_length - i} == {valve.score * (max_length - i)} cum={score}')

print(score)
