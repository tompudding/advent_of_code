import sys


def get_next_item(sequence):
    current = sequence
    total = sequence[-1]

    while len(set(current)) != 1:
        current = [current[i + 1] - current[i] for i in range(len(current) - 1)]
        total += current[-1]

    return total


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file]

sequences = [[int(num) for num in line.split()] for line in lines]

print(sum(get_next_item(sequence) for sequence in sequences))
print(sum(get_next_item(sequence[::-1]) for sequence in sequences))
