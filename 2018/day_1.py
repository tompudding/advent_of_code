import sys

with open(sys.argv[1], "r") as file:
    frequencies = [int(line) for line in file]

print(sum(frequencies))

total = 0

seen = {total}
while True:
    for f in frequencies:
        total += f
        if total in seen:
            print(total)
            raise SystemExit
        seen.add(total)
