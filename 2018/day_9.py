import sys


class Marble:
    def __init__(self, num):
        self.value = num
        self.clockwise = self
        self.anticlockwise = self

    def insert(self, other):
        prev_clockwise = self.clockwise
        prev_clockwise.anticlockwise = other
        self.clockwise = other
        other.anticlockwise = self
        other.clockwise = prev_clockwise

    def remove(self):
        self.clockwise.anticlockwise = self.anticlockwise
        self.anticlockwise.clockwise = self.clockwise

    def step_clockwise(self, num):
        current = self
        for i in range(num):
            current = current.clockwise
        return current

    def step_anticlockwise(self, num):
        current = self
        for i in range(num):
            current = current.anticlockwise
        return current


with open(sys.argv[1], "r") as file:
    parts = file.read().split()
    num_players, num_marbles = int(parts[0]), int(parts[6])
    num_marbles += 1


def run_game(num_players, num_marbles):
    players = [0 for i in range(num_players)]

    current = Marble(0)
    player = 0

    for marble in range(1, num_marbles):
        if (marble % 23) == 0:
            next_current = current.step_anticlockwise(6)
            to_remove = next_current.step_anticlockwise(1)

            players[marble % num_players] += marble + to_remove.value
            to_remove.remove()
            current = next_current
        else:
            new_marble = Marble(marble)
            current.step_clockwise(1).insert(new_marble)
            current = new_marble

    return max(players)


print(run_game(num_players, num_marbles))
print(run_game(num_players, num_marbles * 100))
