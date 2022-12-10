import sys

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

class Chain:
    vectors = {'R' : (1,0),
               'U' : (0,1),
               'L' : (-1,0),
               'D' : (0,-1)}

    def __init__(self, num_knots):
        self.rope = [(0,0) for i in range(num_knots)]
        self.tails = set()

    def step(self, cmd):
        vector = self.vectors[cmd]

        self.rope[0] = add(self.rope[0], vector)

        for i in range(1, len(self.rope)):
            self.rope[i] = self.update(self.rope[i-1], self.rope[i])

        self.tails.add(tuple(self.rope[-1]))

    @staticmethod
    def update(head, tail):
        diff = (head[0] - tail[0], head[1] - tail[1])
        if abs(diff[0]) <= 1 and abs(diff[1]) <= 1:
            return tail
        diff = [x/abs(x) if x else 0 for x in diff]
        return add(tail, diff)

commands = []
with open(sys.argv[1],'r') as file:
    for line in file:
        cmd, num = line.strip().split()
        num = int(num)
        commands.append((cmd, num))

chain = Chain(2)
for cmd, amount in commands:
    for i in range(amount):
        chain.step(cmd)

print(len(chain.tails))

chain = Chain(10)
for cmd, amount in commands:
    for i in range(amount):
        chain.step(cmd)

print(len(chain.tails))
