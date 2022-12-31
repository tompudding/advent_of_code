import enum


class ParameterMode(enum.IntFlag):
    POSITION = 0
    IMMEDIATE = 1


class Instruction:
    out_val = None

    def __init__(self, cpu, program):
        pos = cpu.pc
        self.cpu = cpu
        self.program = program
        self.pos = pos
        assert (program[pos] % 100) == self.opcode
        self.values = program[pos : pos + self.num_ints]
        self.params = self.values[1:]
        mode_mask = program[pos] // 100
        self.modes = []
        for i in range(self.num_ints - 1):
            self.modes.append(mode_mask % 10)
            mode_mask //= 10

        self.out = None

        if self.out_val is not None:
            # If there's multiple values there's always an output I think? Make sure it's in position mode
            self.out = self.values[self.out_val]
            assert self.modes[self.out_val - 1] == ParameterMode.POSITION

    def get_val(self, n):
        mode = ParameterMode(self.modes[n])
        if mode == ParameterMode.POSITION:
            return self.program[self.params[n]]
        elif mode == ParameterMode.IMMEDIATE:
            return self.params[n]
        else:
            raise ValueError("Unrecognised paramater mode")


class BinaryInstruction(Instruction):
    num_ints = 4
    out_val = 3

    def operate(self):
        self.program[self.out] = self.op(self.get_val(0), self.get_val(1))


class Add(BinaryInstruction):
    opcode = 1

    def op(self, a, b):
        return a + b


class Multiply(BinaryInstruction):
    opcode = 2

    def op(self, a, b):
        return a * b


class Input(Instruction):
    opcode = 3
    num_ints = 2
    out_val = 1

    def operate(self):
        self.program[self.out] = self.cpu.get_input()


class Output(Instruction):
    opcode = 4
    num_ints = 2

    def operate(self):
        self.cpu.send_output(self.get_val(0))


class JEQ(Instruction):
    opcode = 5
    num_ints = 3

    def operate(self):
        if self.get_val(0):
            self.cpu.pc = self.get_val(1)
            return True


class JNE(Instruction):
    opcode = 6
    num_ints = 3

    def operate(self):
        if not self.get_val(0):
            self.cpu.pc = self.get_val(1)
            return True


class LT(BinaryInstruction):
    opcode = 7

    def op(self, a, b):
        print(f"lt {a} < {b}")
        return 1 if a < b else 0


class EQ(BinaryInstruction):
    opcode = 8

    def op(self, a, b):
        print(f"eq {a} == {b}")
        return 1 if a == b else 0


class Halt(Instruction):
    opcode = 99
    num_ints = 1

    def operate(self):
        self.cpu.halt()


all_instructions = (Add, Multiply, Input, Output, JEQ, JNE, LT, EQ, Halt)


class IntCode:
    instruction_map = {cls.opcode: cls for cls in all_instructions}

    def __init__(self, program, inputs=[]):
        self.program = program[::]
        self.inputs = inputs[::]
        self.output = []
        self.pc = 0
        self.halted = False

    def halt(self):
        self.halted = True

    def get_input(self):
        assert len(self.inputs) > 0
        return self.inputs.pop(0)

    def send_output(self, value):
        self.output.append(value)

    def run(self):
        self.pc = 0
        while self.pc < len(self.program):
            old_pc = self.pc
            ins = self.instruction_map[self.program[self.pc] % 100](self, self.program)
            if ins.operate():
                # This means the pc was set by the instruction
                assert self.pc != old_pc
                continue
            if self.halted:
                break
            self.pc += ins.num_ints
