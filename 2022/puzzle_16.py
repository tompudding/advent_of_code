import sys
import re
import heapq
import itertools
import time

names = []
valves = []
names_to_index = {}

useful_valves = []

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

def find_best_pressure(max_length, can_turn_on):
    start = (names_to_index['AA'],0,0)
    frontier = []
    heapq.heappush(frontier, (0, start))
    #came_from = {start : None}

    score_so_far = {start : 0}

    best = 0
    max_turned_on = can_turn_on

    while frontier:
        s, node = heapq.heappop(frontier)
        current, length, turned_on = node
        current_valve = valves[current]
        score = score_so_far[node]

        if turned_on == max_turned_on:
           #we're done
           continue

        for next_index, distance in current_valve.neighbours:
            next_valve = valves[next_index]
            if next_valve.score:
                if next_valve.bit & turned_on or 0 == (next_valve.bit & can_turn_on):
                    # We can't turn on the same thing twice
                    continue

            new_length = length + distance
            if new_length > max_length:
                continue

            new_node = (next_index, new_length, turned_on | next_valve.bit)
            new_score = score + ((max_length - new_length) * next_valve.score)

            if new_score > best:
                best = new_score
                best_node = new_node

            if new_node  not in score_so_far or new_score > score_so_far[new_node]:
                score_so_far[new_node] = new_score
                priority = -new_score

                heapq.heappush(frontier, (priority, new_node))
                #came_from[new_node] = node

    #print(best)
    return best

    if 0: #Print the path
        current = best_node

        path = []
        minute = 0
        while current != start:
            index, length, turned_on = current
            path.append((index, names[index]))
            #print(names[index], length, '%x' % turned_on)
            current = came_from[current]
        path.append((names_to_index['AA'], 'AA'))
        path.reverse()

        pressure = 0
        score = 0
        length = 0
        for i, (index, name) in enumerate(path):
            valve = valves[index]
            if i > 0:
                last_index, last_name = path[i-1]
                last_valve = valves[last_index]

                for n,d in last_valve.neighbours:
                    if n == index:
                        distance = d
                        break
                else:
                    raise Jawn()
                length += distance

                score += valve.score * (max_length - length)
            if 0 == valve.score:
                print(name, length)
            else:
                print(f'{name} releases {valve.score} * {max_length - length} == {valve.score * (max_length - length)} cum={score}')


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

# Now we can collapse that graph by excluding the non-useful valves. To do that we need to work out the
# shortest path between all the useful nodes

useful_valves = [valve for valve in valves if valve.flow_rate != 0 or valve.name == 'AA']

shortest_routes = {}

for i, start_valve in enumerate(useful_valves):
    # Now do a BFS from this one, and record the shortest distance to each other useful valve
    frontier = []
    start = start_valve.index
    heapq.heappush(frontier, (0, start))
    came_from = {start : None}
    cost_so_far = {start : 0}

    while frontier:
        s, current = heapq.heappop(frontier)
        current_valve = valves[current]

        for next_index, distance in current_valve.neighbours:
            next_valve = valves[next_index]

            new_cost = cost_so_far[current] + distance
            if next_index not in cost_so_far or new_cost < cost_so_far[next_index]:
                cost_so_far[next_index] = new_cost
                priority = new_cost
                heapq.heappush(frontier, (priority, next_index))
                came_from[next_index] = current

    for j in range(i+1, len(useful_valves)):
        other_valve = useful_valves[j]

        cost = cost_so_far[other_valve.index]

        try:
            shortest_routes[other_valve.index].append( (start_valve.index,cost))
        except KeyError:
            shortest_routes[other_valve.index] = [(start_valve.index,cost)]
        if other_valve.name == 'AA' and other_valve.flow_rate == 0:
            continue
        try:
            shortest_routes[start_valve.index].append( (other_valve.index,cost))
        except KeyError:
            shortest_routes[start_valve.index] = [(other_valve.index,cost)]



for valve in valves:
    if valve.flow_rate == 0 and valve.score == 0:
        #The only one like this that we care about is AA
        if valve.name == 'AA':
            valve.neighbours = shortest_routes[valve.index]
        else:
            valve.neighbours = []
        continue
    if valve.score == 0:
        # This is a valve that can be turned on, so we need to keep that neighbour (it's always the last one by construction
        new_neighbours = shortest_routes[valve.index] + valve.neighbours[-1:]
    else:
        # This is the "turned on" node, so we want the neighbours for the turned off version
        new_neighbours = shortest_routes[valve.index - 1]
    valve.neighbours = new_neighbours

print('collapsed graph')

max_turned_on = 0
for valve in valves:
    max_turned_on |= valve.bit

score = find_best_pressure(30, max_turned_on)
print(score)

#For part 2 we want to try all the partitions of the valves that can be turned on, there should't be too many
pressure_valves = [valve for valve in valves if valve.bit != 0]

scores = {max_turned_on : find_best_pressure(26, max_turned_on)}
max_score = scores[max_turned_on]
best = 0

bitfields = [i for i in range(1<<len(pressure_valves))]
last_print = 0

def count_bits(n):
    num = sum( ((n>>i)&1) for i in range(len(pressure_valves)))

    return abs(num - len(pressure_valves)/2)

bitfields.sort(key=count_bits)


for pos, bitfield in enumerate(bitfields):

    total_score = 0

    done = (pos*100)//len(bitfields)
    if done != last_print:
        print(f'{done}%')
        last_print = done

    can_turn_on = 0
    for i in range(len(pressure_valves)):
        if bitfield & (1 << i):
            can_turn_on |= pressure_valves[i].bit

    for bf in can_turn_on, (max_turned_on ^ can_turn_on):
        try:
            score = scores[bf]
        except KeyError:
            score = find_best_pressure(26, bf)
            scores[bf] = score

        if bf == can_turn_on and score + max_score < best:
            # We don't even need to bother with the other one here
            scores[max_turned_on ^ can_turn_on] = 0
            break

        total_score += score

    if total_score > best:
        best = total_score
        print(f'{best=} a={can_turn_on:x} b={max_turned_on ^ can_turn_on:x} {pos=}')
        for i in range(len(valves)):
            if not valves[i].score:
                continue
            if can_turn_on & valves[i].bit:
                print('ME=',valves[i].name)
            else:
                print('EL=',valves[i].name)

print(best, time.time())
