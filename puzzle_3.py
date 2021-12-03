import sys


def count_bits(counts, word):
    for i, bit in enumerate(word):
        if bit == 1:
            counts[i] += 1


def most_common_at_position(words, pos, tie_break=0):
    count = 0
    for word in words:
        if word[pos] == 1:
            count += 1
    if count > len(words) / 2:
        return 1
    elif count < len(words) / 2:
        return 0
    return tie_break


def to_binary(bits, width):
    answer = 0
    for i, bit in enumerate(bits):
        answer |= bit << (width - 1 - i)
    return answer


def bit_filter(words, most_common_change, tie_break):
    for i in range(width):
        # We want to keep anything that has the most common bit ^ most_common_change at this position
        match_bit = most_common_at_position(words, i, tie_break ^ most_common_change) ^ most_common_change

        words = [word for word in words if word[i] == match_bit]
        if len(words) == 1:
            break
    if len(words) != 1:
        raise SystemExit("Gah")
    return to_binary(words[0], width)


with open(sys.argv[1], "r") as file:
    words = [[int(b) for b in line.strip()] for line in file.readlines()]

width = len(words[0])

gamma = to_binary([most_common_at_position(words, i) for i in range(width)], width)
epsilon = gamma ^ ((1 << width) - 1)
print(gamma * epsilon)

# Let's get the oxygen:
oxygen = bit_filter(words, most_common_change=0, tie_break=1)
co2 = bit_filter(words, most_common_change=1, tie_break=0)

print(oxygen * co2)
