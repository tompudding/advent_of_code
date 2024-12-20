import sys

with open(sys.argv[1], "r") as file:
    polymer = file.read().strip()


def destroys(a, b):
    return a.lower() == b.lower() and a != b


def destroy(x):
    out = []
    pos = 0
    while pos < len(x) - 1:
        if destroys(x[pos], x[pos + 1]):
            pos += 2
            continue
        out.append(x[pos])
        pos += 1
        continue
    if pos < len(x):
        out.append(x[pos])
    return "".join(out)


def count_reduction_old(x):
    current = x
    while True:
        next_item = destroy(current)
        # print(current, next_item)

        if len(next_item) == len(current):
            break
        current = next_item
    return len(current)


def count_reduction(x):
    count = 0
    pos = 0
    destroyed = set()

    while pos < len(x) - 1:
        best_width = 0
        for width in range(len(x)):
            if pos - width < 0 or pos + width + 1 >= len(x):
                break
            if destroys(x[pos - width], x[pos + width + 1]):
                destroyed.add(pos - width)
                destroyed.add(pos + width + 1)
                best_width = width + 1
                continue
            break
        print(pos, best_width)
        if best_width:
            count += best_width * 2
            pos = pos + best_width + 1
        else:
            pos += 1

    return len(x) - len(destroyed)


print(count_reduction(polymer))

best = 10**18
for letter in "abcdefghijklmnopqrstuvwxyz":
    final = polymer.replace(letter, "").replace(letter.upper(), "")
    num = count_reduction_old(final)
    if num < best:
        best = num
        print("removing", letter, best)
