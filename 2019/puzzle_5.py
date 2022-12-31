import sys
import intcode

with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

program = intcode.IntCode(instructions, [1])
program.run()

print(program.output[-1])

program = intcode.IntCode(instructions, [5])
program.run()

print(program.output)
