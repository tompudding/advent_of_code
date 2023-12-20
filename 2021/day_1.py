import os
import sys


def delta(filename, n):
    count = 0
    with open(sys.argv[1], "r") as file:
        data = (int(line.strip(), 10) for line in file)

        window = [next(data) for i in range(n)]

        for n in data:
            if n > window[0]:
                count += 1

            window.pop(0)
            window.append(n)
    return count


print(delta(sys.argv[1], 1))
print(delta(sys.argv[1], 3))
