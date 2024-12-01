import sys
import intcode
import os

class Directions:
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    ALL = {UP, RIGHT, DOWN, LEFT}
    from_char = {'<' : LEFT,
                 '>' : RIGHT,
                 'v' : DOWN,
                 '^' : UP}
    to_char = {value : key for key,value in from_char.items()}

    turns = {UP : {RIGHT : 'R',
                   LEFT : 'L'},
             RIGHT : {UP : 'L',
                      DOWN : 'R'},
             DOWN : {RIGHT : 'L',
                     LEFT : 'R'},
             LEFT : {UP : 'R',
                     DOWN : 'L'}}

class Place:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __hash__(self):
        return hash((self.pos, self.direction))

    def __repr__(self):
        return f'PLACE[{self.pos} {self.direction}]'

    def __lt__(self, other):
        return self.pos < other.pos

class Scaffold:
    def __init__(self, data):
        self.rows = [list(line) for line in data.splitlines()]
        self.grid = {}
        self.walls = set()

        for y, row in enumerate(self.rows):
            for x, cell in enumerate(row):
                self.grid[x, y] = cell
                if cell == '#':
                    self.walls.add((x, y))
                try:
                    self.start = Place((x, y), Directions.from_char[cell])
                except KeyError:
                    pass

    def get_nexii(self):
        total = 0

        nexii = set()

        for x, y in self.walls:
            neighbours = {(x + direction[0], y + direction[1]) for direction in Directions.ALL}

            if len(neighbours & self.walls) == 4:
                total += (x*y)
                nexii.add((x, y))
                self.rows[y][x] = '+'
        return total

    def get_path(self):
        instructions = []

        walked = 0
        pos = self.start
        while True:
            #print(self)
            #input()
            new_pos = (pos.pos[0] + pos.direction[0], pos.pos[1] + pos.direction[1])
            self.rows[pos.pos[1]][pos.pos[0]] = '|' if pos.direction in (Directions.UP, Directions.DOWN) else '='

            if new_pos in self.walls:
                # Mark the last position as walked
                walked += 1
                pos.pos = new_pos
                self.rows[pos.pos[1]][pos.pos[0]] = Directions.to_char[pos.direction]
                continue
            if walked:
                instructions.append(str(walked))
                walked = 0

            for direction,turn in Directions.turns[pos.direction].items():
                new_pos = (pos.pos[0] + direction[0], pos.pos[1] + direction[1])
                if new_pos in self.walls:
                    instructions.append(turn)
                    self.rows[pos.pos[1]][pos.pos[0]] = Directions.to_char[direction]
                    pos.direction = direction
                    break
            else:
                # Hopefully we're done
                return instructions

    def __repr__(self):
        return '\n'.join(''.join(line).replace('.',' ') for line in self.rows)

def compress(path):
    # We know the whole path has to be in subpaths, so loop over the length of the start and end path, one
    # combination of it must leave everything else in the other path

    for start_len in range(4, 11):
        for end_len in range(4, 11):
            A = path[:start_len]
            C = path[-end_len:]
            B = None

            others = set()
            pos = 0
            start_b = None

            while pos < len(path):
                if path[pos:pos+start_len] == A:
                    pos += start_len
                elif path[pos:pos+end_len] == C:
                    pos += end_len
                else:
                    if start_b is None:
                        start_b = pos
                        break
                    pos += 1

            for b_len in range(4, 12):
                B = path[start_b:start_b+b_len]

                # Now if we're done we'll be able to make the whole path out of A,B and C. If not we can try another length of A and C
                final_path = []
                pos = 0
                bad_guess = False
                subpaths = {'A':A,'B':B,'C':C}

                while pos < len(path):
                    for name,chunk in subpaths.items():
                        if path[pos:pos+len(chunk)] == chunk:
                            pos += len(chunk)
                            final_path.append(name)
                            break
                    else:
                        # This wasn't right
                        bad_guess = True
                        break

                if not bad_guess:
                    # yay
                    return final_path, subpaths


    raise CompressionFailed


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

program = intcode.IntCode(instructions, [])

try:
    program.resume()
except intcode.Halted:
    pass

data = ''.join(chr(c) for c in program.output)
scaffold = Scaffold(data)

print(scaffold.get_nexii())

path = scaffold.get_path()
path, subpaths = compress(path)

program = intcode.IntCode(instructions, [])
program.program[0] = 2

#Main:
program.inputs.extend([ord(c) for c in ','.join(path)] + [ord('\n')])
for function in 'ABC':
    program.inputs.extend([ord(c) for c in ','.join(subpaths[function])] + [ord('\n')])

# No thank you to continuous video
program.inputs.extend([ord('n'),ord('\n')])
try:
    program.resume()
except intcode.Halted:
    print(program.output[-1])
