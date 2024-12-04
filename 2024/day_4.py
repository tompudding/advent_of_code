import sys
from utils import Point2D as Point
import enum

class Directions(enum.Enum):
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    UP_RIGHT = UP + RIGHT
    DOWN_RIGHT = DOWN + RIGHT
    DOWN_LEFT = DOWN + LEFT
    UP_LEFT = UP + LEFT

class Grid:
    def __init__(self, lines):
        self.rows = lines
        self.starts = set()

    # Bit of a hack, but return a dict of 1 into the word for matches of the given word in the given directions
    def count_words(self, word, directions):
        matches = {}
        count = 0

        for y,row in enumerate(self.rows):
            for x,char in enumerate(row):
                if char != word[0]:
                    continue
                start = Point(x,y)
                for direction in directions:
                    pos = start
                    for char in word[1:]:
                        pos += direction.value
                        if pos.x < 0 or pos.y < 0:
                            break
                        try:
                            if self.rows[pos.y][pos.x] != char:
                                break
                        except IndexError:
                            break
                    else:
                        #print(f'{word} at {start} in {direction}')
                        try:
                            matches[start + direction.value] += 1
                        except KeyError:
                            matches[start + direction.value] = 1
                        count += 1

        return count, matches


with open(sys.argv[1],'r') as file:
    grid = Grid([line for line in file])

print(grid.count_words('XMAS',Directions)[0])

diagonals = [Directions.DOWN_RIGHT, Directions.DOWN_LEFT, Directions.UP_RIGHT, Directions.UP_LEFT]

count, matches = grid.count_words('MAS',diagonals)
print(len([pos for pos, count in matches.items() if count == 2]))
