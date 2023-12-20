import sys


class Game:
    def __init__(self, line):
        id_part, rest = line.split(":")
        self.id = int(id_part.split()[1])
        colour_index = {"red": 0, "green": 1, "blue": 2}
        self.draws = []

        for draw in rest.split(";"):
            current_draw = [0, 0, 0]
            for cubes in draw.split(","):
                num, colour = cubes.split()
                num = int(num)
                current_draw[colour_index[colour]] += num
            self.draws.append(current_draw)

    def possible(self, total_cubes):
        for draw in self.draws:
            for i in range(3):
                if draw[i] > total_cubes[i]:
                    return False
        return True

    def power(self):
        product = 1

        for i in range(3):
            min_cubes = max(draw[i] for draw in self.draws)
            product *= min_cubes

        return product


games = []
with open(sys.argv[1], "r") as file:
    for line in file:
        games.append(Game(line.strip()))

print(sum(game.id for game in games if game.possible([12, 13, 14])))
print(sum(game.power() for game in games))
