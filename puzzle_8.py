import sys

count = 0

with open(sys.argv[1], "r") as file:
    for line in file:
        patterns, output = (part.split() for part in line.split("|"))
        for word in output:
            if len(word) in [2, 4, 3, 7]:
                count += 1

print(count)


def count(words, char):
    return len([word for word in words if char in word])


def guess(left, digits_to_word, digit, candidates):
    if len(candidates) != 1:
        raise Bobbins  # SystemExit("You messed up")
    digits_to_word[digit] = candidates[0]
    return left - set(candidates)


total = 0
with open(sys.argv[1], "r") as file:
    for line in file:
        patterns, output = (part.split() for part in line.split("|"))
        match = False
        map = {}
        digits_to_word = {}
        easy_lengths = {2: 1, 4: 4, 3: 7, 7: 8}
        left = set()
        for word in patterns:
            try:
                digit = easy_lengths[len(word)]
                map[word] = digit
                digits_to_word[digit] = word
            except KeyError:
                left.add(word)

        # That gives us the easy 4. Next we can deduce what segment represents c and which f
        a = (set(digits_to_word[7]) - set(digits_to_word[1])).pop()

        # c is in 7 and in 8 of the other words, whereas f is in 9
        cf = set(digits_to_word[8]) & set(digits_to_word[1])
        for char in cf:
            if count(patterns, char) == 8:
                c = char
                f = (cf - set(char)).pop()
            else:
                f = char
                c = (cf - set(char)).pop()

        left = guess(left, digits_to_word, 2, [word for word in left if len(word) == 5 and f not in word])

        # Of The remaining 2 length 5 words, 3 has c in it and 5 does not
        left = guess(left, digits_to_word, 3, [word for word in left if len(word) == 5 and c in word])
        left = guess(left, digits_to_word, 5, [word for word in left if len(word) == 5 and c not in word])

        # next let's work out what d is
        bd = set(digits_to_word[4]) - cf

        b = (bd - set(digits_to_word[2])).pop()
        d = (bd - set(b)).pop()

        # Then looking at the remaining length sixers, they're each missing only one character. If it's d, it's 0

        left = guess(left, digits_to_word, 0, [word for word in left if d not in word])

        # If it's c, it's 6
        left = guess(left, digits_to_word, 6, [word for word in left if c not in word])

        # Then only 9 is left
        digits_to_word[9] = left.pop()

        # I was supposed to do this the other way around lol
        words_to_digits = {tuple(sorted(v)): k for k, v in digits_to_word.items()}

        # That's got the digits to word, so count the outputs...
        output = [words_to_digits[tuple(sorted(word))] for word in output]

        # Screw int parsing!
        for pos, val in enumerate(output):
            total += val * (10 ** (3 - pos))


print(total)
