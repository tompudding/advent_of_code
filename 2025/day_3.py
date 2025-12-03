import sys


def best_value(line, num_required):
    best = [0] * num_required

    pos = 0
    line_pos = 0
    while pos < num_required:
        biggest = 0

        for i in range(line_pos, len(line) + 1 - (num_required - pos)):
            num = line[i]
            if num > biggest:
                biggest = num
                best_pos = i

        best[pos] = biggest
        line_pos = best_pos + 1
        pos += 1

    return int("".join(str(d) for d in best))


data = []

with open(sys.argv[1]) as file:
    for line in file:
        data.append([int(c) for c in line.strip()])

print(sum(best_value(line, 2) for line in data))
print(sum(best_value(line, 12) for line in data))
