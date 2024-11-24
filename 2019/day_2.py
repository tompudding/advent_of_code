import sys
import intcode

with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

instructions[1:3] = [12, 2]
# print(list(enumerate(instructions)))

program = intcode.IntCode(instructions)
program.run()

print(program.program[0])

for noun in range(100):
    for verb in range(100):
        instructions[1:3] = [noun, verb]
        program = intcode.IntCode(instructions)
        program.run()
        if program.program[0] == 19690720:
            print(100 * noun + verb)
            raise SystemExit()
