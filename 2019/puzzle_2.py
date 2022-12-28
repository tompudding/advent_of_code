import sys


class Instruction:
    def __init__(self, program, pos):
        self.program = program
        self.pos = pos
        assert program[pos] == self.opcode
        self.values = program[pos : pos + 4]


class BinaryInstruction(Instruction):
    def __init__(self, program, pos):
        super().__init__(program, pos)
        self.in_a, self.in_b, self.out = self.values[1:]

    def operate(self):
        self.program[self.out] = self.op(self.program[self.in_a], self.program[self.in_b])


class Add(BinaryInstruction):
    opcode = 1

    def op(self, a, b):
        return a + b


class Multiply(BinaryInstruction):
    opcode = 2

    def op(self, a, b):
        return a * b


class Halt(Instruction):
    opcode = 99

    def operate(self):
        return True


class IntCode:
    instruction_map = {cls.opcode: cls for cls in (Add, Multiply, Halt)}

    def __init__(self, program):
        self.program = program[::]

        # self.instructions = [self.instruction_map[program[i]](program, i) for i in range(0, len(program), 4)]

    def run(self):
        pos = 0
        while pos < len(self.program):
            ins = self.instruction_map[self.program[pos]](self.program, pos)
            if ins.operate():
                break
            pos += 4


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

instructions[1:3] = [12, 2]
# print(list(enumerate(instructions)))

program = IntCode(instructions)
program.run()

print(program.program[0])

for noun in range(100):
    for verb in range(100):
        instructions[1:3] = [noun, verb]
        program = IntCode(instructions)
        program.run()
        if program.program[0] == 19690720:
            print(100 * noun + verb)
            raise SystemExit()
