import sys


digits_to_segments = {
    "0": "abcefg",
    "1": "cf",
    "2": "acdeg",
    "3": "acdfg",
    "4": "bcdf",
    "5": "abdfg",
    "6": "abdefg",
    "7": "acf",
    "8": "abcdefg",
    "9": "abcdfg",
}


def get_counts(words):
    counts = {}

    for segment in "".join(words):
        try:
            counts[segment] += 1
        except KeyError:
            counts[segment] = 1
    return counts


def get_score(word, segment_counts):
    score = 0
    for segment in word:
        score += segment_counts[segment]

    return score


canonical_scores = {}
canonical_counts = get_counts(digits_to_segments.values())
canonical_scores = {get_score(word, canonical_counts): digit for digit, word in digits_to_segments.items()}

assert len(canonical_scores) == 10


def process_line(line):
    patterns, output = (part.split() for part in line.split("|"))

    segment_counts = get_counts(patterns)

    words_to_digit = {}

    for word in patterns:
        score = get_score(word, segment_counts)
        digit = canonical_scores[score]
        words_to_digit[tuple(sorted(word))] = digit

    output = int("".join([words_to_digit[tuple(sorted(word))] for word in output]))
    return output


count = 0

with open(sys.argv[1], "r") as file:
    for line in file:
        patterns, output = (part.split() for part in line.split("|"))
        for word in output:
            if len(word) in [2, 4, 3, 7]:
                count += 1

print(count)


total = 0
with open(sys.argv[1], "r") as file:
    for line in file:
        total += process_line(line.strip())

print(total)
