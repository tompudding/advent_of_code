import sys

with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file]

digits = [[int(c) for c in line if c in "0123456789"] for line in lines]

total = sum((line[0] * 10 + line[-1] for line in digits))

print(total)

numbers = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parse_digits(line):
    out = []
    pos = 0
    while pos < len(line):
        for num in numbers:
            if line[pos:].startswith(num):
                out.append(numbers[num])
                # They can overlap!
                pos += 1
                break
        else:
            pos += 1

    return out


digits = []

for line in lines:
    digits.append(parse_digits(line))

total = sum((line[0] * 10 + line[-1] for line in digits))

print(total)
