import sys
import intcode

with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

for input_int in [1, 2]:
    program = intcode.IntCode(instructions, [input_int])
    program.run()
    print(program.output[0])
