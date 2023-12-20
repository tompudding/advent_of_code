import sys


class Colony:
    def __init__(self, days):
        self.population = [0 for i in range(9)]

        for day in days:
            self.population[day] += 1

    def step(self):
        # We should use a ring buffer for this really
        budders = self.population.pop(0)
        self.population.append(budders)
        self.population[6] += budders


with open(sys.argv[1], "r") as file:
    state = (int(n) for n in file.read().split(","))
    colony = Colony(state)


for i in range(80):
    colony.step()

print(sum(colony.population))

for i in range(176):
    colony.step()

print(sum(colony.population))
