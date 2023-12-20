import sys

elf = []
elves = []

with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()

        if not line:
            elves.append(elf)
            elf = []
            continue
        amount = int(line.strip())
        elf.append(amount)

if elf:
    elves.append(elf)

elf_amounts = sorted([sum(elf) for elf in elves])
print(elf_amounts[-1])
print(sum(elf_amounts[-3:]))
