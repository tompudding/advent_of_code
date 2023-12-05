import sys


class Card:
    def __init__(self, num, winners, numbers):
        self.num = num
        self.winners = winners
        self.numbers = numbers
        self.num_winners = len(self.winners & self.numbers)


total = 0
cards = []
with open(sys.argv[1], "r") as file:
    for line in file:
        num, rest = line.split(": ")
        num = int(num.split()[1])
        line = rest.strip()

        winners, ours = (set(part.strip().split()) for part in line.split("|"))
        cards.append(Card(num, winners, ours))

for card in cards:
    num_winners = card.num_winners
    if 0 == num_winners:
        continue
    total += 2 ** (num_winners - 1)


print(total)

multiplier = 1
total = 0
decreases = {}


for i, card in enumerate(cards):
    try:
        multiplier -= decreases[i]
    except KeyError:
        pass

    total += multiplier

    if card.num_winners == 0:
        continue

    try:
        decreases[i + card.num_winners + 1] += multiplier
    except KeyError:
        decreases[i + card.num_winners + 1] = multiplier

    multiplier *= 2


print(total)
