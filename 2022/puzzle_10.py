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
        ins = 0
        while ins < len(code):
            current = code[ins]
            end = self.cycle + current.cycles
            while self.cycle < end:
                self.output()
                self.cycle += 1
                if self.cycle == self.next_sample:
                    self.samples.append(self.x * self.cycle)
                    self.next_sample += 40

            current.perform(self)
            ins += 1
            
    def output(self):
        #print(f'{self.x=} {self.cycle=}')
        current_x = self.cycle % 40
        end = '\n' if current_x == 39 else ''
        char = '.'
        char = '#' if abs(self.x - current_x) <= 1 else '.'
        print(char,end=end)

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

# let's simulate
cpu = Cpu()
print('Part 2:')
cpu.run(commands)
print(f'Part 1 = {sum(cpu.samples)}')

