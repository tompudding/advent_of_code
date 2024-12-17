import sys


class Halted(Exception):
    pass


class Instruction:
    out_val = None
    num_ints = 2

    def __init__(self, cpu, program, pos=None):
        if pos is None:
            pos = cpu.pc
        self.cpu = cpu
        self.program = program
        self.pos = pos
        self.operand = program[pos + 1]

    def combo(self):
        match self.operand:
            case num if num <= 3:
                return num
            case 4:
                return self.cpu.A
            case 5:
                return self.cpu.B
            case 6:
                return self.cpu.C
            case 7:
                raise BadOperand()

    def __repr__(self):
        return f"{self.nemonic:3s} : {self.operand=}"


class Adv(Instruction):
    opcode = 0
    nemonic = "ADV"

    def operate(self):
        self.cpu.A = self.cpu.A // (1 << self.combo())


class Bxl(Instruction):
    opcode = 1
    nemonic = "BXL"

    def operate(self):
        self.cpu.B ^= self.operand


class Bst(Instruction):
    opcode = 2
    nemonic = "BST"

    def operate(self):
        self.cpu.B = self.combo() & 7


class Jnz(Instruction):
    opcode = 3
    nemonic = "JNZ"

    def operate(self):
        if self.cpu.A:
            self.cpu.pc = self.operand
            return True


class Bxc(Instruction):
    opcode = 4
    nemonic = "BXC"

    def operate(self):
        self.cpu.B ^= self.cpu.C


class Out(Instruction):
    opcode = 5
    nemonic = "OUT"

    def operate(self):
        self.cpu.send_output(self.combo() & 7)


class Bdv(Instruction):
    opcode = 6
    nemonic = "BDV"

    def operate(self):
        self.cpu.B = self.cpu.A // (1 << self.combo())


class Cdv(Instruction):
    opcode = 7
    nemonic = "CDV"

    def operate(self):
        self.cpu.C = self.cpu.A // (1 << self.combo())


all_instructions = (Adv, Bxl, Bst, Jnz, Bxc, Out, Bdv, Cdv)


class IntCode:
    instruction_map = {cls.opcode: cls for cls in all_instructions}

    def __init__(self, program, A):
        self.program = program
        self.output = []
        self.pc = 0
        self.halted = False
        self.A = A
        self.B = 0
        self.C = 0

    def halt(self):
        self.halted = True

    def send_output(self, value):
        self.output.append(value)

    def run(self):
        self.pc = 0
        try:
            self.resume()
        except Halted:
            pass

    def step(self, num):
        count = 0
        while (num is None) or (count < num):
            count += 1
            old_pc = self.pc
            try:
                ins = self.instruction_map[self.program[self.pc]](self, self.program)
            except IndexError:
                raise Halted()
            if ins.operate():
                # This means the pc was set by the instruction
                assert self.pc != old_pc
                continue
            if self.halted:
                raise Halted()
                break
            self.pc += ins.num_ints

    def resume(self):
        return self.step(None)

    def __repr__(self):
        out = [f"Register {name}: {val}" for name, val in (("A", self.A), ("B", self.B), ("C", self.C))]
        out.append(f"PC: {self.pc}")
        out.append(str(self.output))

        pos = 0

        while pos < len(self.program):
            try:
                ins = self.instruction_map[self.program[pos] % 100](self, self.program, pos)
                jump = ins.num_ints
            except KeyError:
                ins = f"UNK : {self.program[pos]}"
                jump = 1

            out.append(f"{pos:3d} : {ins}")
            pos += jump

        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    instructions = []
    registers = {}

    for line in file:
        if "Register" in line:
            reg, num = [part.strip() for part in line.strip().split(":")]
            registers[reg.split()[1]] = int(num)
        elif "Program:" in line:
            instructions.extend([int(v) for v in line.split(": ")[1].strip().split(",")])

program = IntCode(instructions, registers["A"])
print(program)

try:
    while True:
        program.step(1)
        # print(program)
        # print()
except Halted:
    pass

print(",".join((str(v) for v in program.output)))

# We'll build it up a digit at a time, working from the right


A = 0
index = len(instructions)
digits = [0 for i in range(len(instructions) + 1)]

while index >= 0:
    while digits[index] < 8:
        program = IntCode(instructions, (A << 3) | digits[index])

        try:
            program.resume()
        except Halted:
            pass

        if program.output[0] == instructions[index - 1]:
            break
        digits[index] += 1
    else:
        # No match
        digits[index] = 0
        index += 1
        digits[index] += 1
        A >>= 3
        continue

    A = (A << 3) | digits[index]
    if program.output == instructions:
        break
    index -= 1

print(A)

# Program does this:
# B = A % 8
# B ^= 1
# C = A // (1 << B)
# B ^= (C ^ 5)
# A = A // 8
# OUT B
# if( a == 0 ): done
# else start again
# 4532307133267275
# 4532357133267275 is too high
# 164546529291965 is too high
# 164541160582845
