import sys


def mix(data, moves):
    for pos in range(len(moves)):
        pos = pos % len(moves)
        if data[moves[pos]] == 0:
            continue

        old_pos = moves[pos]
        new_pos = moves[pos] + data[moves[pos]]

        item = data.pop(old_pos)

        new_pos = (new_pos) % len(data)

        data.insert(new_pos, item)

        lower = min(new_pos, old_pos)
        upper = max(new_pos, old_pos)
        change = 1 if new_pos <= old_pos else -1

        # TODO: Do this without traversing the whole list dummy
        for i in range(len(moves)):
            if moves[i] < lower:
                continue
            if moves[i] == old_pos:
                moves[i] += new_pos - old_pos

            elif moves[i] <= upper:
                moves[i] += change

    return data, moves


with open(sys.argv[1], "r") as file:
    data = [int(line.strip()) for line in file.readlines()]

orig_data = data[::]
moves = list(range(len(data)))

# Part 1
data, moves = mix(data, moves)

zero = data.index(0)
print(sum([data[(zero + i) % len(data)] for i in (1000, 2000, 3000)]))

# Part 2
data = [item * 811589153 for item in orig_data]
moves = list(range(len(data)))

for i in range(10):
    data, moves = mix(data, moves)

zero = data.index(0)
print(sum([data[(zero + i) % len(data)] for i in (1000, 2000, 3000)]))
