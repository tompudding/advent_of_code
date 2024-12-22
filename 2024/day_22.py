import sys
from collections import defaultdict
import itertools


def op(n):
    n = (n ^ (n << 6)) & 0xFFFFFF
    n = (n ^ (n >> 5)) & 0xFFFFFF
    n = (n ^ (n << 11)) & 0xFFFFFF
    return n


def do_op(n, m):
    for i in range(m):
        n = op(n)
    return n


def op_sequence(start, num_required):
    yield start % 10
    num = start
    for i in range(num_required):
        num = op(num)
        yield num % 10


def get_deltas(seq, num):
    for i in range(2000 - num):
        deltas = []
        yield tuple([(b) - (a) for a, b in itertools.pairwise(seq[i : i + num + 1])]), seq[i + num]


with open(sys.argv[1], "r") as file:
    numbers = [int(line) for line in file]

print(sum(do_op(num, 2000) for num in numbers))

winnings = defaultdict(list)


# For part two can we store the sell price of each 4 difference sequence?
for number in numbers:
    num_winnings = {}
    for deltas, price in get_deltas(tuple(op_sequence(number, 2000)), 4):
        if deltas in num_winnings:
            # The monkeys always take the first match
            continue
        num_winnings[deltas] = price

    for deltas, price in num_winnings.items():
        winnings[deltas].append(price)

winnings = [(deltas, sum(prices), prices) for deltas, prices, in winnings.items()]
winnings.sort(key=lambda x: x[1])


print(winnings[-1][1])
