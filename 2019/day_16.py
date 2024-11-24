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


    def __repr__(self):
        return ''.join((str(d) for d in self.sequence))

with open(sys.argv[1], 'r') as file:
    seq = Sequence(file.read().strip())

for i in range(100):
    seq.transform()
print(seq)
