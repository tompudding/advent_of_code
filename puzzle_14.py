import sys
import collections


class Polymer:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.pair_counts = {}
            self.start_chain = file.readline().strip()

            for i in range(len(self.start_chain) - 1):
                pair = self.start_chain[i : i + 2]
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
        # This counts each character twice, except for the ends, so start them at 1 so we can divide the whole lot by 2.
        counts = {self.start_chain[0]: 1, self.start_chain[-1]: 1}

        for pair, count in self.pair_counts.items():
            for char in pair:
                try:
                    counts[char] += count
                except KeyError:
                    counts[char] = count
        return sorted(counts.values())


polymer = Polymer(sys.argv[1])

for i in range(10):
    polymer.step()

counts = polymer.counts()

print((counts[-1] - counts[0]) >> 1)

for i in range(30):
    polymer.step()
counts = polymer.counts()

print((counts[-1] - counts[0]) >> 1)
