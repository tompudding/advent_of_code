import sys

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

class World:
    wall = '#'
    air = ' '
    sand = 'o'
    sand_start = (500, 0)
    sand_steps = ((0, 1), (-1,1), (1,1))
    
    def __init__(self, floor=False):
        self.grid = {}
        self.top_left = None
        self.bottom_right = None
        self.top_left = list(self.sand_start)
        self.bottom_right = [self.sand_start[0]+1, self.sand_start[1]+1]
        self.grid = {self.sand_start : self.sand}
        self.has_floor = floor
        self.floor = 0 if self.has_floor else None
        self.building = True
        self.starts = [self.sand_start]
                          

    def add(self, pos, item):
        if pos[0] < self.top_left[0]:
            self.top_left[0] = pos[0]
        if pos[1] < self.top_left[1]:
            self.top_left[1] = pos[1]
        if pos[0] >= self.bottom_right[0]:
            self.bottom_right[0] = pos[0]+1
        if pos[1] >= self.bottom_right[1]:
            self.bottom_right[1] = pos[1] + 1

        #we only change the floor position during building
        if self.building and self.has_floor and pos[1] +2 > self.floor:
            self.floor = pos[1] + 2
            self.bottom_right[1] = max(self.bottom_right[1], self.floor+1)

        self.grid[pos] = item

    def add_rocks(self, a, b):
        if a[0] == b[0]:
            #This is a vertical line
            if b[1] < a[1]:
                a,b = b,a
            diff = b[1] - a[1]
            for i in range(diff+1):
                self.add((a[0], a[1] + i),self.wall)
        elif a[1] == b[1]:
            #Horiz
            if b[0] < a[0]:
                a,b = b,a
            diff = b[0] - a[0]
            for i in range(diff+1):
                self.add((a[0] + i, a[1]),self.wall)

    def fix_floor(self):
        self.building = False

    def __repr__(self):
        lines = []

        for row in range(self.top_left[1], self.bottom_right[1]):
            line = []
            for col in range(self.top_left[0], self.bottom_right[0]):
                try:
                    item = self.grid[(col, row)]
                except KeyError:
                    item = self.air
                line.append(item)
            lines.append(''.join(line))
        return '\n'.join(lines)
        return ''

    def in_abyss(self, pos):
        if self.has_floor and pos == self.sand_start:
            return True
        return pos[1] < self.top_left[1] or pos[1] >= self.bottom_right[0]

    def step(self):
        while self.starts:
            pos = self.starts[-1]
            for diff in self.sand_steps:
                new_pos = add(pos, diff)

                if new_pos in self.grid or self.has_floor and new_pos[1] >= self.floor:
                    continue
                if self.in_abyss(new_pos):
                    return None

                pos = new_pos
                self.starts.append(pos)
                break
            else:
                #If we didn't break it means we couldn't place the sand, and the current position is final
                if pos == self.starts[-1]:
                    self.starts.pop(-1)

                if not self.starts:
                    return None
                self.add(pos, self.sand)
                return True

world = World()
rocks = []

with open(sys.argv[1],'r') as file:
    for line in file:
        line = line.strip()
        endpoints = [[int(v) for v in point.split(',')] for point in line.split(' -> ')]
        rocks.append(endpoints)

for endpoints in rocks:
    for i in range(len(endpoints)-1):
        world.add_rocks(endpoints[i], endpoints[i+1])
            

steps = 0
while placed := world.step():
    steps += 1

print(steps)

world = World(floor=True)

for endpoints in rocks:
    for i in range(len(endpoints)-1):
        world.add_rocks(endpoints[i], endpoints[i+1])
world.fix_floor()

steps = 0
while placed := world.step():
    steps += 1

print(steps+1)
