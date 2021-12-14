import sys
import collections


class Polymer:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.pair_counts = {}
            start_chain = file.readline().strip()

            for i in range(len(start_chain) - 1):
                pair = start_chain[i : i + 2]
                try:
                    self.pair_counts[pair] += 1
                except KeyError:
                    self.pair_counts[pair] = 1

            self.rules = {}

            for line in file:
                line = line.strip()
                if not line:
                    continue
                pair, dest = line.split(" -> ")
                self.rules[pair] = (pair[0] + dest, dest + pair[1])

    def step(self):
        self.new_counts = {}

        for pair, count in self.pair_counts.items():
            for new_pair in self.rules[pair]:
                try:
                    self.new_counts[new_pair] += count
                except KeyError:
                    self.new_counts[new_pair] = count

        self.pair_counts = self.new_counts

    def counts(self):
        # This counts each character twice, except for the last one.
        counts = {}

        for pair, count in self.pair_counts.items():
            for char in pair:
                try:
                    counts[char] += count
                except KeyError:
                    counts[char] = count
        return sorted(counts.values())


polymer = Polymer(sys.argv[1])

for i in range(40):
    polymer.step()

print(polymer.new_counts)
counts = polymer.counts()


print((counts[-1] - counts[0]) >> 1)
