import enum


class InputStall(Exception):
    pass


class Halted(Exception):
    pass


class ParameterMode(enum.IntFlag):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Instruction:
    out_val = None

    def __init__(self, cpu, program, pos=None):
        if pos is None:
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
            # If there's multiple values there's always an output I think? Make sure it's in position/relative
            # mode
            self.out = self.values[self.out_val]
            assert self.modes[self.out_val - 1] in [ParameterMode.POSITION, ParameterMode.RELATIVE]

    def get_val(self, n):
        mode = ParameterMode(self.modes[n])
        if mode == ParameterMode.POSITION:
            return self.cpu.get_memory(self.params[n], 1)[0]
        elif mode == ParameterMode.IMMEDIATE:
            return self.params[n]
        elif mode == ParameterMode.RELATIVE:
            return self.cpu.get_memory(self.cpu.relative_base + self.params[n], 1)[0]
        else:
            raise ValueError("Unrecognised paramater mode")

    def get_out(self):
        if self.modes[self.out_val - 1] == ParameterMode.RELATIVE:
            return self.out + self.cpu.relative_base
        return self.out

    def __repr__(self):
        return f"{self.nemonic:3s} : {self.values=} {self.modes=}"


class BinaryInstruction(Instruction):
    num_ints = 4
    out_val = 3

    def operate(self):
        self.cpu.set_memory(self.get_out(), [self.op(self.get_val(0), self.get_val(1))])
        # self.program[self.out] = self.op(self.get_val(0), self.get_val(1))


class Add(BinaryInstruction):
    opcode = 1
    nemonic = "ADD"

    def op(self, a, b):
        return a + b


class Multiply(BinaryInstruction):
    opcode = 2
    nemonic = "MUL"

    def op(self, a, b):
        return a * b


class Input(Instruction):
    opcode = 3
    num_ints = 2
    out_val = 1
    nemonic = "INP"

    def operate(self):
        self.cpu.set_memory(self.get_out(), [self.cpu.get_input()])
        # self.program[self.out] = self.cpu.get_input()


class Output(Instruction):
    opcode = 4
    num_ints = 2
    nemonic = "OUT"

    def operate(self):
        self.cpu.send_output(self.get_val(0))


class JEQ(Instruction):
    opcode = 5
    num_ints = 3
    nemonic = "JEQ"

    def operate(self):
        if self.get_val(0):
            self.cpu.pc = self.get_val(1)
            return True


class JNE(Instruction):
    opcode = 6
    num_ints = 3
    nemonic = "JNE"

    def operate(self):
        if not self.get_val(0):
            self.cpu.pc = self.get_val(1)
            return True


class LT(BinaryInstruction):
    opcode = 7
    nemonic = "LT"

    def op(self, a, b):
        return 1 if a < b else 0


class EQ(BinaryInstruction):
    opcode = 8
    nemonic = "EQ"

    def op(self, a, b):
        return 1 if a == b else 0


class AdjustRelativeBase(Instruction):
    opcode = 9
    num_ints = 2
    nemonic = "REL"

    def operate(self):
        self.cpu.relative_base += self.get_val(0)


class Halt(Instruction):
    opcode = 99
    num_ints = 1
    nemonic = "HLT"

    def operate(self):
        self.cpu.halt()


all_instructions = (Add, Multiply, Input, Output, JEQ, JNE, LT, EQ, AdjustRelativeBase, Halt)


class IntCode:
    instruction_map = {cls.opcode: cls for cls in all_instructions}

    def __init__(self, program, inputs=[]):
        self.program = program[::] + [0] * 10000
        self.inputs = inputs[::]
        self.output = []
        self.pc = 0
        self.halted = False
        self.relative_base = 0

    def halt(self):
        self.halted = True

    def get_input(self):
        if len(self.inputs) == 0:
            raise InputStall()
        return self.inputs.pop(0)

    def send_output(self, value):
        self.output.append(value)

    def get_memory(self, addr, length):
        if addr + length > len(self.program):
            print(f"Expanding program up to len {addr+length}")
            extra = (addr + length) - len(self.program)
            self.program.extend([0] * extra)

        return self.program[addr : addr + length]

    def set_memory(self, addr, data):
        self.program[addr : addr + len(data)] = data

    def run(self):
        self.pc = 0
        try:
            self.resume()
        except Halted:
            pass

    def resume(self):
        while self.pc < len(self.program):
            old_pc = self.pc
            ins = self.instruction_map[self.program[self.pc] % 100](self, self.program)
            if ins.operate():
                # This means the pc was set by the instruction
                assert self.pc != old_pc
                continue
            if self.halted:
                raise Halted()
                break
            self.pc += ins.num_ints

    def __repr__(self):
        out = []

        pos = 0

        while pos < len(self.program):
            try:
                ins = self.instruction_map[self.program[pos] % 100](self, self.program, pos)
            except KeyError:
                out.append("UNK")
                pos += 1
                continue
            out.append(repr(ins))
            pos += ins.num_ints

        return "\n".join(out)
