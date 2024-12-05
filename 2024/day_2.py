import sys


def get_sign(value):
    if value == 0:
        return 0
    return value // abs(value)


def remove(data, pos):
    # At the start we may have gotten the direction wrong if the first was bad, so also include the previous
    # one in that case
    start = 0 if pos == 1 else pos
    end = pos + 2
    for i in range(start, end):
        yield data[:i] + data[i + 1 :]


def safe(data, allowed_bad=0):
    direction = None
    for i in range(len(data) - 1):
        diff = data[i + 1] - data[i]

        if abs(diff) > 3 or abs(diff) < 1:
            if allowed_bad > 0:
                # Try it without both of the offending numbers
                return any(safe(removed, allowed_bad - 1) for removed in remove(data, i))

            return False

        sign = get_sign(diff)

        if direction is None:
            direction = sign
            continue

        if direction != sign:
            if allowed_bad > 0:
                # Try it without both of the offending numbers. If i == 1 we might also get away with a different direction
                return any(safe(removed, allowed_bad - 1) for removed in remove(data, i))

            return False

    return True


with open(sys.argv[1], "r") as file:
    reports = [line for line in file]

print(sum((safe(report, allowed_bad=0) for report in reports)))
print(sum((safe(report, allowed_bad=1) for report in reports)))
