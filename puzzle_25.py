import sys

class Cucumber:
    dir = None
    def __init__(self, pos):
        self.pos = pos


    def move(self, grid):
        new_pos = ((self.pos[0] + self.dir[0]) % grid.width, (self.pos[1] + self.dir[1]) % grid.height)
        if new_pos in grid.full_grid:
            return 0
        self.pos = new_pos
        return 1

class EastCucumber(Cucumber):
    dir = (1, 0)

class SouthCucumber(Cucumber):
    dir = (0, 1)

class Grid:
    def __init__(self, lines):
        self.easters = []
        self.southers = []
        self.width = len(lines[0].strip())
        self.height = len(lines)

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == '>':
                    self.easters.append(EastCucumber((x, y)))
                elif char == 'v':
                    self.southers.append(SouthCucumber((x,y)))

        self.east_grid = {cuke.pos for cuke in self.easters}
        self.south_grid = {cuke.pos for cuke in self.southers}
        self.full_grid = self.east_grid | self.south_grid

    def __repr__(self):
        out = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                if (x,y) in self.east_grid:
                    line.append('>')
                elif (x,y) in self.south_grid:
                    line.append('v')
                else:
                    line.append('.')
            out.append(''.join(line))
        return '\n'.join(out)

    def step(self):
        num_stepped = 0

        for cuke in self.easters:
            num_stepped += cuke.move(self)

        self.east_grid = {cuke.pos for cuke in self.easters}
        self.full_grid = self.east_grid | self.south_grid
        
        for cuke in self.southers:
            num_stepped += cuke.move(self)

        self.south_grid = {cuke.pos for cuke in self.southers}
        self.full_grid = self.east_grid | self.south_grid

        return num_stepped


with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

grid = Grid(lines)

num_stepped = 1
print(grid)
print()
total_steps = 0
while num_stepped:
    num_stepped = grid.step()
    total_steps += 1
    #print(num_stepped)
    #print(grid)
    #print()
print(total_steps)
