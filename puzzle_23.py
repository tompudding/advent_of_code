import sys


class Rooms:
    # This is our coordinate system:
    #
    # ###################################
    # # 0  1  2  3  4  5  6  7  8  9 10 #
    # ###### 13 ## 15 ## 17 ## 19 #######
    #      # 24 ## 26 ## 28 ## 30 #
    #      ########################
    #
    # A state is a list of 8 positions, A, A, B, etc.
    # By not distinguishing the two letters that are the same we're going to be increasing the state space by a lot. Hmmm
    neighbours = {
        0: {1},
        1: {0, 2},
        2: {13, 3},
        3: {2, 4},
        4: {3, 15, 5},
        5: {4, 6},
        6: {5, 17, 7},
        7: {6, 8},
        8: {7, 19, 9},
        10: {9},
        13: {2, 24},
        15: {4, 26},
        17: {6, 28},
        19: {8, 30},
        24: {13},
        26: {15},
        28: {17},
        30: {19},
    }

    rooms = [{13 + 11 * i + 2 * j for i in range(4)} for j in range(4)]
    all_rooms = rooms[0] | rooms[1] | rooms[2] | rooms[3]
    no_stop = {2, 4, 6, 8}
    hallway = {i for i in range(11)}
    final = (13, 24, 15, 26, 17, 28, 19, 30)
    bottom = {i for i in range(24, 31, 2)}
    scores = (1, 1, 10, 10, 100, 100, 1000, 1000)
    destinations = {
        0: (3, 5, 7, 9, 10),
        1: (3, 5, 7, 9, 10),
        3: (0, 1, 5, 7, 9, 10),
        5: (0, 1, 3, 7, 9, 10),
        7: (0, 1, 3, 5, 9, 10),
        9: (0, 1, 3, 5, 7),
    }
    target_rooms = {
        0: (13, 24),
        1: (13, 24),
        2: (15, 26),
        3: (15, 26),
        4: (17, 28),
        5: (17, 28),
        6: (19, 30),
        7: (19, 30),
    }
    coords = {i: (i, 0) for i in range(11)} | {
        13: (2, 1),
        15: (4, 1),
        17: (6, 1),
        19: (8, 1),
        24: (2, 2),
        26: (4, 2),
        28: (6, 2),
        30: (8, 2),
    }

    def __init__(self, state):
        self.state = tuple(sorted(state[0:2]) + sorted(state[2:4]) + sorted(state[4:6]) + sorted(state[6:8]))
        self.state_set = set(self.state)
        self.best = None

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

    def path(self, piece, start, target):
        # We simply want to change X to the right place, then change y
        coord = self.coords[start]
        target_coord = self.coords[target]
        path = [start]
        pos = start
        if start in self.hallway:
            # We're in the hallway so we need to start with x first
            x_dir = 1 if target_coord[0] > coord[0] else -1
            path = [pos]
            while pos != target_coord[0]:
                pos += x_dir
                if pos in self.state_set:
                    return None
                path.append(pos)

            while pos != target:
                # This means we're descending into a room
                pos += 11
                if pos in self.state_set:
                    return None
                path.append(pos)
        else:
            # We're starting in a room, so we have to go to the hallway first
            while pos >= 11:
                pos -= 11
                path.append(pos)

            x_dir = 1 if target_coord[0] > pos else -1
            while pos != target_coord[0]:
                pos += x_dir
                if pos in self.state_set:
                    return None
                path.append(pos)

            # Then we're descending into a room
            while pos != target:
                # This means we're descending into a room
                pos += 11
                if pos in self.state_set:
                    return None
                path.append(pos)

        return (len(path) - 1) * self.scores[piece]

    def __repr__(self):
        out = ["#############", "#...........#", "###.#.#.#.###", "  #.#.#.#.#  ", "  #########  "]
        out = [[c for c in line] for line in out]
        for piece, pos in enumerate(self.state):
            coord = self.coords[pos]
            out[coord[1] + 1][coord[0] + 1] = "AABBCCDD"[piece]

        return "\n".join(["".join(line) for line in out])


best = 2 ** 32


def solve(state, previous_states, last_moved, total_score):
    global best
    # Let's try looping over the possible moves we can take. We won't move the same piece as last time,
    # and we won't move anything in the hallway unless it crosses a door

    if state.state in previous_states:
        return

    if total_score > best:
        return

    if state.state == Rooms.final:
        best = total_score
        return

    for piece in range(8):
        if piece == last_moved:
            continue

        pos = state.state[piece]

        # Firstly, we can only move this piece if it's not trapped
        if pos in Rooms.bottom and pos - 11 in state.state_set:
            continue

        if pos in Rooms.target_rooms[piece] and pos in Rooms.bottom or state.state[piece ^ 1] == pos + 11:
            continue

        # OK We'll move this piece
        moved = piece

        # If we're in the hallway our options are another hallway position (as long as it crosses a door),
        # or the correct room (if it's either empty or has the same type of piece as me

        targets = []
        # We can only enter a room if it's either empty and we go to the bottom, or it already has the correct type at the bottom and we go to the top
        for room_pos in Rooms.target_rooms[piece]:
            if room_pos not in Rooms.bottom:
                if state.state[piece ^ 1] == room_pos + 11:
                    targets.append(room_pos)
            else:
                # This will get caught in the pathing
                targets.append(room_pos)

        if pos not in Rooms.hallway:
            targets.extend(list(Rooms.hallway - Rooms.no_stop))

        for target in targets:
            piece_name = "AABBCCDD"[piece]
            score = state.path(piece, pos, target)
            if score is None:
                continue

            # This is where we're moving
            previous_states.add(state.state)

            # make a new target state
            new_state = list(state.state[::])
            new_state[piece] = target
            new_state = Rooms(new_state)
            # print(new_state)

            for solution in solve(new_state, previous_states, piece, total_score + score):
                yield solution


with open(sys.argv[1], "r") as file:
    lines = file.readlines()

rooms = Rooms.from_lines(lines)
print(rooms)


for solution in solve(rooms, set(), None, 0):
    # print(solution)
    pass

print(best)
