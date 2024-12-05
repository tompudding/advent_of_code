import sys
from utils import Point2D as Point
import enum
import collections


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
    def __init__(self, rows):
        self.grid = {}
        self.starts = collections.defaultdict(list)
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                p = Point(x, y)
                self.grid[p] = char
                self.starts[char].append(p)

    # Bit of a hack, but return a dict of 1 into the word for matches of the given word in the given directions
    def count_words(self, word, directions):
        matches = collections.defaultdict(int)
        count = 0

        for start in self.starts[word[0]]:
            for direction in directions:
                grid_word = (self.grid[start + direction.value * (i + 1)] for i, char in enumerate(word[1:]))

                try:
                    if all(
                        grid_letter == word_letter for grid_letter, word_letter in zip(grid_word, word[1:])
                    ):
                        # print(f'{word} at {start} in {direction}')
                        matches[start + direction.value] += 1
                        count += 1
                except KeyError:
                    pass

        return count, matches


with open(sys.argv[1], "r") as file:
    grid = Grid([line for line in file])

print(grid.count_words("XMAS", Directions)[0])

diagonals = [Directions.DOWN_RIGHT, Directions.DOWN_LEFT, Directions.UP_RIGHT, Directions.UP_LEFT]

count, matches = grid.count_words("MAS", diagonals)
print(len([pos for pos, count in matches.items() if count == 2]))
