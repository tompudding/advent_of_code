import sys
import math


class Deck:
    def __init__(self, size):
        self.size = size
        self.cards = list(range(self.size))

    def deal_into(self):
        self.cards = list(reversed(self.cards))

    def cut(self, n):
        self.cards = self.cards[n:] + self.cards[:n]

    def deal_increment(self, n):
        new_cards = [0] * self.size
        for i, c in enumerate(self.cards):
            new_cards[(i * n) % self.size] = c
        self.cards = new_cards

    def index(self, n):
        return self.cards.index(n)

    def process(self, command):
        if command == "deal into new stack":
            self.deal_into()
            return

        parts = command.split()
        n = int(parts[-1])
        if parts[0] == "cut":
            self.cut(n)
        else:
            self.deal_increment(n)

    def __repr__(self):
        return repr(self.cards)


class CleverDeck(Deck):
    def __init__(self, size):
        self.start = 0
        self.stride = 1
        self.size = size

    def deal_into(self):
        self.cut(-1)
        self.stride = self.size - self.stride

    def cut(self, n):
        self.start = (self.start + (n * self.stride)) % self.size

    def deal_increment(self, n):
        self.stride = (self.stride * pow(n, -1, self.size)) % self.size

    def index(self, target):
        # We can just generate them until we run into this one, because hopefully this function should never
        # get called on the big deck
        x = self.start
        for n in range(self.size):
            if x == target:
                return n
            x = (x + self.stride) % self.size

    def get(self, index):
        return (self.start + self.stride * index) % self.size

    def multiply(self, n):
        # Our current stride and start represent one iteration of our commands, what will they be after n iterations?
        # We can do this by repeated squaring.
        added = 0

        start = self.start
        stride = self.stride

        self.start = 0
        self.stride = 1

        while n:
            if n & 1:
                self.start = (start + (self.start * stride)) % self.size
                self.stride = (self.stride * stride) % self.size

            new_start = (start * (stride + 1)) % self.size
            new_stride = (stride * stride) % self.size
            start = new_start
            stride = new_stride
            n >>= 1

    def __repr__(self):
        out = [(self.start + self.stride * n) % self.size for n in range(self.size)]
        return repr(out)


deck = CleverDeck(10007)

with open(sys.argv[1], "r") as file:
    commands = [line.strip() for line in file]

for command in commands:
    deck.process(command)


print(deck.index(2019))

deck = CleverDeck(119315717514047)

for command in commands:
    deck.process(command)

deck.multiply(101741582076661)

print(deck.get(2020))
