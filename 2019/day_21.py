import sys
import intcode
import os


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])


def format_program(cmds):
    return [ord(n) for n in ("\n".join(cmds) + "\n")]


program = intcode.IntCode(
    instructions, format_program(["OR A T", "AND B T", "AND C T", "NOT T J", "AND D J", "WALK"])
)

try:
    program.resume()

except intcode.Halted:
    pass

if program.output[-1] > 0x100:
    print(program.output[-1])
    program.output = program.output[:-1]


program = intcode.IntCode(
    instructions,
    format_program(
        [
            "OR A T",
            "AND B T",
            "AND C T",
            "NOT T J",
            "AND D J",
            "AND H J",
            "NOT A T",
            "OR T J",
            "RUN",
        ]
    ),
)

try:
    program.resume()
except intcode.Halted:
    pass

if program.output[-1] > 0x100:
    print(program.output[-1])
    program.output = program.output[:-1]
