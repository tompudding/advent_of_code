class Instruction:
    def __init__(self, program, pos):
        self.program = program
        self.pos = pos
        assert program[pos] == self.opcode
        self.values = program[pos : pos + self.num_ints]


class BinaryInstruction(Instruction):
    num_ints = 4

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
    num_ints = 1

    def operate(self):
        return True


class IntCode:
    instruction_map = {cls.opcode: cls for cls in (Add, Multiply, Halt)}

    def __init__(self, program):
        self.program = program[::]

    def run(self):
        pos = 0
        while pos < len(self.program):
            ins = self.instruction_map[self.program[pos]](self.program, pos)
            if ins.operate():
                break
            pos += ins.num_ints
