import sys


total = 0
cards = []
with open(sys.argv[1], "r") as file:
    for line in file:
        num, rest = line.split(": ")
        line = rest.strip()

        winners, ours = (set(part.strip().split()) for part in line.split("|"))
        cards.append(len(winners & ours))

for num_winners in cards:
    if 0 == num_winners:
        continue
    total += 2 ** (num_winners - 1)


print(total)

multiplier = 1
total = 0
decreases = {}


for i, num_winners in enumerate(cards):
    try:
        multiplier -= decreases[i]
    except KeyError:
        pass

    total += multiplier

    if num_winners == 0:
        continue

    try:
        decreases[i + num_winners + 1] += multiplier
    except KeyError:
        decreases[i + num_winners + 1] = multiplier

    multiplier *= 2


print(total)
