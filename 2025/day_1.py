import sys


def process_line(line):
    num = int(line[1:])
    full_turns = num // 100
    remainder = num % 100
    return full_turns, -remainder if line[0] == "L" else remainder


with open(sys.argv[1], "r") as file:
    data = [process_line(line.strip()) for line in file]

pos = 50
password = 0

for full_turns, num in data:
    pos = (pos + num) % 100
    password += pos == 0

print(password)

pos = 50
password = 0

for full_turns, num in data:
    password += full_turns
    if pos != 0 and (pos + num >= 100 or pos + num <= 0):
        password += 1
    pos = (pos + num) % 100

print(password)
