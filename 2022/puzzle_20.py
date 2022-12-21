import sys

with open(sys.argv[1], "r") as file:
    data = [int(line.strip()) * 811589153 for line in file.readlines()]

pos = 0
done = 0

moves = list(range(len(data)))

print(data)

for pos in range(len(moves) * 10):
    pos = pos % len(moves)
    # print(f"{pos=} {moves[pos]=} {data[moves[pos]]=}")
    if data[moves[pos]] == 0:
        # print(data, moves)
        continue
    old_pos = moves[pos]
    new_pos = moves[pos] + data[moves[pos]]
    # if new_pos <= 0:
    #     # It can never go on the end after underflowing
    #     new_pos -= 1
    # if new_pos >= len(data):
    #     new_pos += 1

    item = data.pop(old_pos)

    new_pos = (new_pos) % len(data)

    data.insert(new_pos, item)

    # item = moves.pop(old_pos)
    # moves.insert(new_pos, item)

    # for i in range(old_pos, new_pos):
    #    moves[

    if new_pos > old_pos:
        for i in range(len(moves)):
            if moves[i] < old_pos:
                continue
            if moves[i] == old_pos:
                moves[i] += new_pos - old_pos

            elif moves[i] <= new_pos:
                moves[i] -= 1
    else:
        for i in range(len(moves)):
            if moves[i] < new_pos:
                continue
            if moves[i] == old_pos:
                moves[i] += new_pos - old_pos
            elif moves[i] <= old_pos:
                moves[i] += 1

    #     if new_pos <= moves[i]:
    #         moves[i] += 1

    # print(f"{old_pos=} {new_pos=}")
    # print(data, moves)

    # for i in range(len(moves)):
    #     if new_pos >= moves[i]:
    #         moves[i] -= 1

    # print(data, moves)

zero = data.index(0)


print(sum([data[(zero + i) % len(data)] for i in (1000, 2000, 3000)]))
# break
# 0:
#  0  1  2  3  4  5  6
#  1  2 -3  3 -2  0  4

# 1:
#  1  0  2  3  4  5  6
#  2  1 -3  3 -2  0  4

# 2:
#  0  2  1  3  4  5  6
#  1 -3  2  3 -2  0  4

# 3:
#  0  1  4  2  3  5  6
#  1  2  3 -2 -3  0  4

# 5:
#   0  1  3  5  2  4  6
#   1  2 -2 -3  0  3  4

# 6:
#   1  2  3  5  0  4  6
#  -2  1  2 -3  0  3  4

# 1 -3 2 3 -2 0 4

# 0 1 2 3 4 5 6
# 2 0 1 3 4 5 6
