import sys

# I expect part 2 is to play 10**40 games of this or something, but let's brute force first anyway


def move(start, amount):
    return ((start + amount - 1) % 10) + 1


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.start_pos = pos
        self.score = 0

    def move(self, amount):
        self.pos = move(self.pos, amount)
        self.score += self.pos


class Dice:
    def __init__(self):
        self.num = 1
        self.rolled = 0

    def roll(self):
        out = self.num
        self.num += 1
        self.rolled += 1
        return out


players = []

with open(sys.argv[1], "r") as file:
    for line in file:
        pos = int(line.strip().split(":")[1])
        players.append(Player(pos))

dice = Dice()

while all(player.score < 1000 for player in players):
    for player in players:
        player.move(sum((dice.roll() for i in range(3))))

        if player.score >= 1000:
            break

loser = sorted([player.score for player in players])[0]

print(dice.rolled * loser)

sums = {}
for a in (1, 2, 3):
    for b in (1, 2, 3):
        for c in (1, 2, 3):
            try:
                sums[a + b + c] += 1
            except KeyError:
                sums[a + b + c] = 1

lookup = {}


def get_win_counts(positions, score_needed, turn):
    key = positions, score_needed, turn
    try:
        out = lookup[key]
        return out
    except KeyError:
        pass

    wins = [0, 0]

    for roll, count in sums.items():
        new_positions = list(positions)
        new_positions[turn] = move(positions[turn], roll)
        if new_positions[turn] >= score_needed[turn]:
            # The player will win with this roll
            wins[turn] += count
            continue
        else:
            new_score_needed = list(score_needed)
            new_score_needed[turn] -= new_positions[turn]
            new_wins = get_win_counts(tuple(new_positions), tuple(new_score_needed), turn ^ 1)

            for i in 0, 1:
                wins[i] += count * new_wins[i]

    lookup[key] = wins
    return wins


positions = tuple([player.start_pos for player in players])
print(sorted(get_win_counts(positions, (21, 21), 0))[1])
