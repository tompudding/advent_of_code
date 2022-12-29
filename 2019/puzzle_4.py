import sys


def digits(n):
    out = []
    for i in range(6):
        out.insert(0, n % 10)
        n //= 10
    if n:
        print(out, n)
        raise SystemExit("n too big")
    return out


def skip(current):
    # We can skip on to the first legal number
    for i in range(1, len(current)):
        if current[i] < current[i - 1]:
            current[i] = current[i - 1]


def is_legal(current):
    for i in range(1, len(current)):
        if current[i] == current[i - 1]:
            return True
    return False


def is_legal_part_two(current):
    for i in range(1, len(current)):
        if (
            current[i] == current[i - 1]
            and ((i < 2) or current[i] != current[i - 2])
            and ((i >= len(current) - 1) or (current[i] != current[i + 1]))
        ):
            return True
    return False


def advance(n):

    pos = len(n) - 1

    while pos > 0:
        n[pos] = (n[pos] + 1) % 10
        if n[pos] >= n[pos - 1]:
            break
        pos -= 1
    if pos == 0:
        n[pos] += 1

    skip(n)


def calculate(start, end, check):
    current = digits(start)
    end_d = digits(end)

    skip(current)

    count = 0

    while current < end_d:
        if check(current):
            count += 1

        advance(current)

    return count


with open(sys.argv[1], "r") as file:
    start, end = (int(v) for v in file.readlines()[0].strip().split("-"))

print(calculate(start, end, is_legal))
print(calculate(start, end, is_legal_part_two))
