import sys
import heapq

def heuristic(a, b):
    # Let's go for a very simple number of state matches
    return sum(x != y for x,y in zip(a.state, b.state))

class Rooms:
    # This is our coordinate system:
    #
    # ###################################
    # # 0  1  2  3  4  5  6  7  8  9 10 #
    # ###### 13 ## 15 ## 17 ## 19 #######
    #      # 24 ## 26 ## 28 ## 30 #
    # OPT  # 35 ## 37 ## 39 ## 41 #
    # OPT  # 46 ## 48 ## 50 ## 52 #
    #      ########################
    #
    # A state is a list of 8 positions, A, A, B, etc.
    # By not distinguishing the two letters that are the same we're going to be increasing the state space by a lot. Hmmm

    no_stop = {2, 4, 6, 8}
    hallway = {i for i in range(11)}
    final = (13, 24, 15, 26, 17, 28, 19, 30)
    scores = (1, 1, 10, 10, 100, 100, 1000, 1000)
    levels = 2
    to_hallway_moves = [(0, 2), (10, 2), (1, 1), (9, 1), (3, 0), (5, 0), (7, 0)]
    piece_mask = 0xe
    above = {pos:{pos - (i+1)*11 for i in range(pos//11)} for pos in final}
    below = {pos:{pos + (i+1)*11 for i in range(2 - pos//11)} for pos in final}

    target_rooms = {
        0: {13, 24},
        1: {13, 24},
        2: {15, 26},
        3: {15, 26},
        4: {17, 28},
        5: {17, 28},
        6: {19, 30},
        7: {19, 30},
    }
    coords = {i: (i, 0) for i in range(11)}
    coords.update({
        13: (2, 1),
        15: (4, 1),
        17: (6, 1),
        19: (8, 1),
        24: (2, 2),
        26: (4, 2),
        28: (6, 2),
        30: (8, 2),
    })

    def __init__(self, state):
        self.state = tuple(sorted(state[0:2]) + sorted(state[2:4]) + sorted(state[4:6]) + sorted(state[6:8]))
        self.state_set = set(self.state)
        self.best = None

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.state < other.state


    @staticmethod
    def from_lines(lines):
        # We'll only ever construct from a string when all the things are in Rooms
        state = [0 for i in range(8)]
        coord = 13
        for line_num in range(2, 4):
            for pos in (3, 5, 7, 9):
                letter = lines[line_num][pos]
                index = (ord(letter) - ord("A")) * 2
                if state[index] == 0:
                    state[index] = coord
                else:
                    state[index + 1] = coord
                coord += 2
                if coord == 21:
                    coord = 24

        return Rooms(tuple(state))

    def piece_at(self, pos):
        try:
            index = self.state.index(pos)
            return index // self.levels
        except ValueError:
            return None
        

    def path(self, piece, start, target):
        # We simply want to change X to the right place, then change y
        coord = self.coords[start]
        target_coord = self.coords[target]
        #path = [start]
        count = 0
        pos = start
        if start in self.hallway:
            # We're in the hallway so we need to start with x first
            x_dir = 1 if target_coord[0] > coord[0] else -1
            #path = [pos]
            while pos != target_coord[0]:
                pos += x_dir
                if pos in self.state_set:
                    return None
                count += 1

            while pos != target:
                # This means we're descending into a room
                pos += 11
                if pos in self.state_set:
                    return None
                count += 1
        else:
            # We're starting in a room, so we have to go to the hallway first
            while pos >= 11:
                pos -= 11
                count += 1
                if pos in self.state_set:
                    return None

            x_dir = 1 if target_coord[0] > pos else -1
            while pos != target_coord[0]:
                pos += x_dir
                if pos in self.state_set:
                    return None
                count += 1

            # Then we're descending into a room
            while pos != target:
                # This means we're descending into a room
                pos += 11
                if pos in self.state_set:
                    return None
                count += 1

        return (count) * self.scores[piece]

    def moves(self):
        for piece in range(len(self.state)):
            pos = self.state[piece]


            # Firstly, we can only move this piece if it's not trapped

            try:
                if self.above[pos] & self.state_set:
                    continue
            except KeyError:
                pass


            # Then if we're in the right room and all the things below us are also right, we cannot move

            normal_piece = piece // (self.levels)

            if pos in self.target_rooms[piece]:
                #below = {pos + (i+1)*11 for i in range(self.levels - pos//11)}
                if all(self.piece_at(below_pos) == normal_piece for below_pos in self.below[pos]):
                    continue


            # OK We'll move this piece
            moved = piece

            # If we're in the hallway our options are another hallway position (as long as it crosses a door),
            # or the correct room (if it's either empty or has the same type of piece as me

            #targets = []
            # We can only enter a room if it's either empty and we go to the bottom, or it already has the correct type at the bottom and we go to the top

            taken_in_room = [self.piece_at(room_pos) for room_pos in self.target_rooms[piece] if room_pos != pos]
            taken_in_room = [taken for taken in taken_in_room if taken is not None]

            if all((piece == normal_piece for piece in taken_in_room)):
                open_in_room = [room_pos for room_pos in self.target_rooms[piece] if room_pos not in self.state_set]
                #print('BB',open_in_room)
                if len(open_in_room) >= 1:
                    #There's an open spot, but we can only take it if all the others in that position are of the right piece
                    yield piece, max(open_in_room)
                    #targets.append((max(open_in_room), 1))

                #print('xx')
        
            if pos not in self.hallway:
                for target, pref in self.to_hallway_moves:
                    yield piece, target
                #targets.extend(self.to_hallway_moves)

    def neighbours(self):
        for piece, target in self.moves():
            pos = self.state[piece]
            score = self.path(piece, pos, target)
            if score is None:
                continue

            # This is where we're moving
            #if self.state in previous_states:
            #    continue
            #previous_states[self.state] = (len(previous_states), total_score+score)

            # make a new target state
            new_state = list(self.state[::])
            new_state[piece] = target
            new_state = self.__class__(new_state)

            yield new_state, score


        #for target, preference in targets:

         #   moves.append((piece, target, preference))

    #moves.sort( key= lambda item: item[0])
    #moves.sort( key= lambda item: item[2], reverse=True)


    def __repr__(self):
        out = ["#############", "#...........#", "###.#.#.#.###", "  #.#.#.#.#  ", "  #########  "]
        out = [[c for c in line] for line in out]
        for piece, pos in enumerate(self.state):
            coord = self.coords[pos]
            out[coord[1] + 1][coord[0] + 1] = "AABBCCDD"[piece]

        return "\n".join(["".join(line) for line in out])

class PartTwo(Rooms):
    levels = 4
    final = [tuple((k+i*11 for i in range(4))) for k in (13, 15, 17, 19)]
    final = final[0] + final[1] + final[2] + final[3]
    piece_mask = 0xc
    target_rooms = {
        0: {13, 24, 35, 46},
        4: {15, 26, 37, 48},
        8: {17, 28, 39, 50},
        12: {19, 30, 41, 52},
    }
    scores = (1, 1, 1, 1, 10, 10, 10, 10, 100, 100, 100, 100, 1000, 1000, 1000, 1000)
    for j in range(0, 16, 4):
        for i in range(1,4):
            target_rooms[j+i] = target_rooms[j]

    coords = {i: (i, 0) for i in range(11)}
    coords.update({13+i+j*11: (2+i, 1+j) for i in range(0,8,2) for j in range(4)})
    print(coords)
    above = {pos:{pos - (i+1)*11 for i in range(pos//11)} for pos in final}
    below = {pos:{pos + (i+1)*11 for i in range(4 - pos//11)} for pos in final}


    def __init__(self, state):
        self.state = tuple(sorted(state[0:4]) + sorted(state[4:8]) + sorted(state[8:12]) + sorted(state[12:16]))
        self.state_set = set(self.state)
        self.best = None

    @staticmethod
    def from_lines(lines):
        # We'll only ever construct from a string when all the things are in Rooms
        state = [0 for i in range(16)]
        coord = 13
        for line_num in range(2, 4):
            for pos in (3, 5, 7, 9):
                letter = lines[line_num][pos]
                index = (ord(letter) - ord("A")) * 4
                if state[index] == 0:
                    state[index] = coord
                else:
                    state[index + 1] = coord
                coord += 2
                if coord == 21:
                    coord = 46

        #Then we have to add some manually
        state[2] = 30
        state[3] = 39
        state[6] = 28
        state[7] = 37
        state[10] = 26
        state[11] = 41
        state[14] = 24
        state[15] = 35

        return PartTwo(tuple(state))

    def __repr__(self):
        out = ["#############", "#...........#", "###.#.#.#.###", "  #.#.#.#.#  ","  #.#.#.#.#  ","  #.#.#.#.#  ", "  #########  "]
        out = [[c for c in line] for line in out]
        for piece, pos in enumerate(self.state):
            coord = self.coords[pos]
            out[coord[1] + 1][coord[0] + 1] = "AAAABBBBCCCCDDDD"[piece]

        return "\n".join(["".join(line) for line in out])


best = 2 ** 32

all_time = {}

actual_path=[(3,10),(0,0),(1,9),(1,7),(0,1), (2,39), (2,28), (1, 5), (3, 3), (1,48), (1, 37), (1,26), (2,17), (0,9), (3,52), (1,15), (3,41), (3, 30), (0,35), (0, 24)]

def solve_dfs(state, last_moved, solution):
    global best
    # Let's try looping over the possible moves we can take. We won't move the same piece as last time,
    # and we won't move anything in the hallway unless it crosses a door

    #if state.state in previous_states:
    #    return
    #if(len(solution) > 12):
    #    print(len(solution))
    #    print(solution[-1])

    #if state.state in all_time:
    #    return all_time[state.state]

    if state.state == state.final:
        total = 0

        for step, cost in solution:
            total += cost
        if total < best:
            print(f'{total=}')
            best = total
            #print(step)
            #print('*'*80)
        return 0, []

    if state.state in all_time:
        return all_time[state.state]
    best_cost = None
    best_solution = None

    #if len(solution) == 22:
    #    print(state)
            
    for new_state, score in state.neighbours():
        ##HAX

        #if len(solution)-1 < len(actual_path):
        #    actual_normal_piece, actual_target = actual_path[len(solution)-1]
        #    normal_piece = piece // (state.levels)
        #    if len(solution) == 1:
        #        print(piece, normal_piece, target, actual_normal_piece, actual_target)
        #    if normal_piece != actual_normal_piece or target != actual_target:
        #        continue
        ##
        #print(piece,target)


        new_cost, new_solution = solve_dfs(new_state, None, solution + [(new_state, score)])
        if new_cost is None:
            continue
        #print('AAA')
        #print(state)
        #print(new_solution)

        new_cost += score
        if best_cost is None or new_cost < best_cost:
            best_cost = new_cost
            best_solution = [(new_state, score)] + new_solution


    if best_cost is None:
        #print(len(solution))
        return None, None

    all_time[state.state] = best_cost, best_solution

    return best_cost, best_solution

def solve_bfs(start):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    final_state = start.__class__(start.final)

    while frontier:
        s, current = heapq.heappop(frontier)

        if current == final_state:
            print('Done')
            break

        for next_state, cost in current.neighbours():
            new_cost = cost_so_far[current] + cost
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic(final_state, next_state)
                #print(priority, next_state)
                heapq.heappush(frontier, (priority, next_state))
                came_from[next_state] = current
                               
    # reconstruct the path
    current = final_state

    path = []
    cost = cost_so_far[final_state]
    while current != start:
        #cost += self.grid[current]
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return cost, path

            

with open(sys.argv[1], "r") as file:
    lines = file.readlines()

rooms = Rooms.from_lines(lines)
print(rooms)

if 0:
    #cost, solution = solve_dfs(rooms, None, [(rooms,0)])
    cost, solution = solve_bfs(rooms)
    print(cost)
    total = 0
    for step in solution:
        print(step)
        print()
    raise SystemExit



print('Go for part 2...')


best = 2**32
rooms = PartTwo.from_lines(lines)
print(rooms)
all_time = {}

cost, solution = solve_bfs(rooms)

print(cost)
total = 0
for step in solution:
    total += cost
    print(step)
    print()
raise SystemExit


print(best)
print(rooms)
