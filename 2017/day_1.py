import sys

with open(sys.argv[1], "r") as file:
    data = [int(v) for v in file.read().strip()]

total = 0
for i in range(len(data)):
    if data[i] == data[(i + 1) % len(data)]:
        total += data[i]

print(total)

total = 0
for i in range(len(data)):
    if data[i] == data[(i + (len(data) // 2)) % len(data)]:
        total += data[i]

print(total)
