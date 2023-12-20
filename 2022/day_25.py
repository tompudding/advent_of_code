import sys


class Snafu:
    char_to_val = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    val_to_char = {v: k for k, v in char_to_val.items()}

    def __init__(self, txt):
        self.txt = txt
        self.num = 0

        for i, char in enumerate(reversed(txt)):
            self.num += (5 ** i) * self.char_to_val[char]

    def __add__(self, other):
        out = Snafu("")
        out.num = self.num + other.num
        txt = []
        num = out.num
        while num:
            last = num % 5
            if last <= 2:
                char = f"{last}"
            else:
                last -= 5
                char = self.val_to_char[last]
            num -= last
            num //= 5
            txt.insert(0, char)
        out.txt = "".join(txt)

        return out

    def __repr__(self):
        return self.txt


snafus = []
with open(sys.argv[1], "r") as file:
    for line in file:
        snafus.append(line.strip())

snafus = [Snafu(txt) for txt in snafus]

for snafu in snafus:
    print(snafu)

total = Snafu("")
for snafu in snafus:
    total += snafu
print(total)
