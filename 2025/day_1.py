import sys


def process_line(line):
    num = int(line[1:])
    full_turns = num // 100
    remainder = num % 100
    return full_turns, -remainder if line[0] == "L" else remainder


def get_password(data, count_turns):
    pos = 50
    password = 0

    for full_turns, num in data:
        if count_turns:
            password += full_turns
            if pos != 0 and (pos + num >= 100 or pos + num <= 0):
                password += 1
        else:
            password += 0 == ((pos + num) % 100)
        pos = (pos + num) % 100

    return password


with open(sys.argv[1], "r") as file:
    data = [process_line(line.strip()) for line in file]

print(get_password(data, False))
print(get_password(data, True))
