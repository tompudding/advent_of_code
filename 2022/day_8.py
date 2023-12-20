import sys

class Grid:
    def __init__(self, filename):
        self.grid = []
        self.positions = {}
        with open(filename, 'r') as file:
            for row,line in enumerate(file):
                self.grid.append([int(tree) for tree in line.strip()])
                for col,tree in enumerate(self.grid[row]):
                    try:
                        self.positions[tree].append( (row, col))
                    except KeyError:
                        self.positions[tree] = [(row, col)]

        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def num_visible(self):
        #First we say that nothing is visible
        invisible = {(row,col) for row in range(1, self.height-1) for col in range(1, self.width-1)}

        def check(row, col, tallest):
            if self.grid[row][col] > tallest:
                #This one is visible
                try:
                    invisible.remove((row,col))
                except KeyError:
                    pass
                tallest = self.grid[row][col]
            return tallest

        #Cast rays from the left...
        for row in range(1, self.height-1):
            tallest = self.grid[row][0]
            for col in range(1, self.width-1):
                tallest = check(row, col, tallest)

        #from the right
        for row in range(1, self.height-1):
            tallest = self.grid[row][self.width-1]
            for col in range(self.width-2,0,-1):
                tallest = check(row, col, tallest)

        #from the top
        for col in range(1, self.width-1):
            tallest = self.grid[0][col]
            for row in range(1, self.height-1):
                tallest = check(row, col, tallest)

        #from the bottom
        for col in range(1, self.width-1):
            tallest = self.grid[self.height-1][col]
            for row in range(self.height-1, 0, -1):
                tallest = check(row, col, tallest)

        return self.width*self.height - len(invisible)

    def sight_score(self, row, col):
        height = self.grid[row][col]
        #print(height)

        right = left = up = down = 0
        #cast right
        for x in range(col+1, self.width):
            right += 1
            if self.grid[row][x] >= height:
                break

        #cast left
        for x in range(col-1, -1, -1):
            left += 1
            if self.grid[row][x] >= height:
                break

        #cast down
        for y in range(row+1, self.height):
            down += 1
            if self.grid[y][col] >= height:
                break

        #cast up
        for y in range(row-1, -1, -1):
            up += 1
            if self.grid[y][col] >= height:
                break
        #print(up, left, right, down)
        return right * left * up * down
            
    def best_sight_score(self):
        #There is surely a better way to do this...
        return max(self.sight_score(row, col) for row in range(1, self.height-1) for col in range(1, self.width-1))


grid = Grid(sys.argv[1])

print(grid.num_visible())
print(grid.best_sight_score())
