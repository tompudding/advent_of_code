import sys

base = [0, 1, 0, -1]

def get_transform_digit(level, digit):
    return base[((digit + 1) // level) % len(base)]

def get_transform_sequence(level):
    pos = 0
    while True:
        yield get_transform_digit(level, pos)
        pos += 1

def last_digit(n):
    if n >= 0:
        return n % 10
    else:
        return (10 - (n % 10)) % 10

class Sequence:
    def __init__(self, sequence):
        self.sequence = [int(n) for n in sequence]

    def transform(self):
        new_seq = []
        for i in range(len(self.sequence)):
            total = 0
            for (s, t) in zip(self.sequence, get_transform_sequence(i+1)):
                total += s * t

            new_seq.append(last_digit(total))

        self.sequence = new_seq

    def mega_transform(self):
        # A B
        # C D
        #
        # D = Sum(B...)
        # C = A + D

        # Start at the end and work backwards. The last digit always stays the same
        for pos in range(len(self.sequence)-2, -1, -1):
            self.sequence[pos] = (self.sequence[pos+1] + self.sequence[pos]) % 10


    def __repr__(self):
        return ''.join((str(d) for d in self.sequence))

with open(sys.argv[1], 'r') as file:
    orig = file.read().strip()
    seq = Sequence(orig)

# The strick for part 2 is that the base sequence is always just a sum in the second half (as the -1s will get pushed back to the end), so each term is the sum of the terms above it,
# e.g:

# A | B | C
# A | B + C | C

# So for any particular phase, the last digit is the same, and then we can build the previous digit from the
# sum of the one above it and the one to its right. We only care about the numbers backwards from the end
# until our offset, so shrink the list so we only have to worry about what we need

offset = int(orig[:7])
x = offset % len(orig)
extra_copies = (len(orig)*10000 - offset - (len(orig)-x) )//len(orig)

seq = Sequence(orig[x:] + orig*extra_copies)
print(len(seq.sequence))

for i in range(100):
    seq.mega_transform()

print(''.join(str(d) for d in seq.sequence[:8]))
