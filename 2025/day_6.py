import sys
import itertools


def prod(factors):
    total = 1
    for num in factors:
        total *= num
    return total


def transform(item):
    match item:
        case "+":
            return sum
        case "*":
            return prod
        case _:
            return int(item)


def compute_worksheet(sheet):
    total = 0
    for row in sheet:
        total += row[-1](row[:-1])
    return total


sheet = []

with open(sys.argv[1]) as file:
    for line in file:
        sheet.append([transform(v) for v in line.strip().split()])

sheet = [[row[i] for row in sheet] for i in range(len(sheet[0]))]

print(compute_worksheet(sheet))

# For part 2 we'll reload the file because we threw away important information doh
sheet = []

with open(sys.argv[1]) as file:
    for line in file:
        sheet.append(list(line[:-1]))

width = max(len(line) for line in sheet)
for line in sheet:
    while len(line) < width:
        line.append(" ")

sheet = [[row[i] for row in sheet] for i in range(len(sheet[0]))]
# Add in an empty line so we'll terminate the count correctly
sheet.append([" "])

total = 0
args = []
for col in sheet:
    # Blank line means we've finished collecting arguments, so output
    if set(col) == {" "}:
        total += func(args)
        args = []
        continue
    # Otherwise the first line will tell us which accumulator to use
    if col[-1] == "*":
        func = prod
    elif col[-1] == "+":
        func = sum
    # The rest of the line is always the number
    args.append(int("".join(col[:-1])))

print(total)
