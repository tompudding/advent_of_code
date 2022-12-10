import sys

class Instruction:
    cycles = None

    def perform(cpu):
        return

class Noop(Instruction):
    cycles = 1

class Add(Instruction):
    cycles = 2
    def __init__(self, amount):
        self.amount = int(amount)

    def perform(self, cpu):
        cpu.x += self.amount

class Cpu:
    def __init__(self):
        self.cycle = 0
        self.x = 1
        self.next_sample = 20
        self.samples = []

    def run(self,code):
        for instruction in code:
            self.cycle += instruction.cycles
            while self.cycle >= self.next_sample:
                self.samples.append(self.x*self.next_sample)
                self.next_sample += 40
            instruction.perform(self)

commands = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('noop'):
            commands.append(Noop)
        elif line.startswith('addx'):
            cmd, amount = line.split()
            commands.append(Add(amount))
        else:
            raise SystemExit(f'Unexpected Command {line}')

# Part 1, let's simulate
cpu = Cpu()
cpu.run(commands)
print(sum(cpu.samples))

