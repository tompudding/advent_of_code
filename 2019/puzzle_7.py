import sys
import intcode
import itertools

max_phase = 5


def advance(phases):
    for i in range(len(phases)):
        phases[i] = (phases[i] + 1) % max_phase
        if phases[i] > 0:
            return False
    return True


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])


phases = [0 for i in range(5)]
max_output = 0

for phases in itertools.permutations(list(range(5))):
    programs = [intcode.IntCode(instructions, [0]) for i in range(5)]
    for phase, program in zip(phases, programs):
        program.inputs[0] = phase

    programs[0].inputs.append(0)

    for i, program in enumerate(programs):
        program.run()
        if i + 1 < len(programs):
            programs[i + 1].inputs.append(program.output.pop(0))

    if programs[-1].output[0] > max_output:
        max_output = programs[-1].output[0]
        best = "".join(f"{n}" for n in phases)

print(best, max_output)

max_output = 0

for phases in itertools.permutations(list(range(5, 10))):
    programs = [intcode.IntCode(instructions, [0]) for i in range(5)]

    for phase, program in zip(phases, programs):
        program.inputs[0] = phase

    # print(programs[0])
    # break

    programs[0].inputs.append(0)

    stall = True
    while stall:
        stall = False
        for i, program in enumerate(programs):
            try:
                program.resume()
            except intcode.InputStall:
                stall = True

            if len(program.output) > 0:
                programs[(i + 1) % len(programs)].inputs.append(program.output.pop(0))

    if programs[0].inputs[-1] > max_output:
        max_output = programs[0].inputs[-1]
        best = "".join(f"{n}" for n in phases)


print(best, max_output)
