import sys

chunks = {"<": ">", "[": "]", "(": ")", "{": "}"}

score = {")": 3, "]": 57, "}": 1197, ">": 25137}
part_two_score = {")": 1, "]": 2, "}": 3, ">": 4}


def scan_line(line):
    stack = []

    for char in line:
        if char in chunks:
            stack.append(char)
            continue
        if char == chunks[stack[-1]]:
            # This is a legit closer
            stack.pop()
            continue
        else:
            # It's bad
            return char, None

    return None, [chunks[char] for char in stack[::-1]]


def closer_score(stack):
    total = 0

    for char in stack:
        total *= 5
        total += part_two_score[char]
    return total


part_one = 0
with open(sys.argv[1], "r") as file:
    for line in file:
        corrupted, stack = scan_line(line.strip())

        if not corrupted:
            continue

        part_one += score[corrupted]

print(part_one)

part_two = []
with open(sys.argv[1], "r") as file:
    for line in file:
        corrupted, stack = scan_line(line.strip())

        if corrupted:
            continue

        part_two.append(closer_score(stack))

part_two.sort()
print(part_two[len(part_two) // 2])
