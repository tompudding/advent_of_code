import os
import sys


def delta(filename, n):

    count = 0
    with open(sys.argv[1], "r") as file:
        buffer = [int(file.readline().strip(), 10) for i in range(n)]

        for line in file:
            try:
                n = int(line.strip(), 10)
            except:
                continue

            if n > buffer[0]:
                count += 1

            buffer.pop(0)
            buffer.append(n)
    return count


print(delta(sys.argv[1], 1))
print(delta(sys.argv[1], 3))
