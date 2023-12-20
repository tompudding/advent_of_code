import sys
import re

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

monkies = []

bigmod = 1

class Monkey:
    
    def __init__(self, lines):
        # Num
        self.num = int(re.match('Monkey (\d+):',lines[0]).groups()[0])

        # Items
        self.items = [int(v.strip()) for v in lines[1].split('Starting items: ')[1].split(',')]

        # Operation
        op = lines[2].split('Operation: new = old ')[1]
        if op[0] == '*':
            self.op = mul

        elif op[0] == '+':
            self.op = add
        else:
            raise ValueError(f'Unexpected operation {op[0]}')

        # Operand
        operand = op[1:].strip()

        if operand == 'old':
            self.operand = None
        else:
            self.operand = int(op[1:].strip())

        # Test
        self.test = int(lines[3].split('Test: divisible by ')[1])

        self.throw_to = [int(lines[n].split('throw to monkey ')[1]) for n in (4,5)]

        self.inspections = 0

    def step(self):
        # We loop over each of our items and dispatch them

        for item in self.items:
            operand = self.operand if self.operand is not None else item
            old_item = item
            item = (self.op(item,  operand) // divide ) % bigmod
            self.inspections += 1
            if (item % self.test) == 0:
                to = self.throw_to[0]
            else:
                to = self.throw_to[1]

            monkies[to].items.append(item)
        self.items = []
            
            
        

monkey_lines = []


with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()
        if 'Monkey' in line and monkey_lines:
            monkies.append(Monkey(monkey_lines))
            monkey_lines = [line]
            continue
        elif line:
            monkey_lines.append(line)
        
if monkey_lines:
    monkies.append(Monkey(monkey_lines))

start_items = []

for monkey in monkies:
    bigmod *= monkey.test
    start_items.append(monkey.items[::])

#Part 1
divide = 3

for round in range(20):
    for monkey in monkies:
        monkey.step()

inspections = sorted([monkey.inspections for monkey in monkies])
print(inspections[-1]*inspections[-2])

#Part 2
divide = 1

for i,monkey in enumerate(monkies):
    monkey.inspections = 0
    monkey.items = start_items[i][::]

for round in range(10000):
    for monkey in monkies:
        monkey.step()

inspections = sorted([monkey.inspections for monkey in monkies])
print(inspections[-1]*inspections[-2])
