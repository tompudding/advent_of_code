import sys
import intcode


class Directions:
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

    turn_right = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
    turn_left = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
    turns = [turn_left, turn_right]


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])


def run_robot(instructions, start_colour):
    program = intcode.IntCode(instructions, [start_colour])
    painted = set()
    painted_ever = set()
    pos = (0, 0)
    direction = Directions.UP
    output_pos = 0
    num_painted = 0

    # print(program)

    while not program.halted:
        try:
            program.resume()
        except intcode.InputStall:
            # It wants the colour of the current panel

            if len(program.output) > 0:
                colour, turn = program.output
                painted_ever.add(pos)
                if colour == 1:
                    painted.add(pos)
                elif colour == 0 and pos in painted:
                    painted.remove(pos)

                direction = Directions.turns[turn][direction]
                pos = (pos[0] + direction[0], pos[1] + direction[1])

                program.output = []
            program.inputs.append(1 if pos in painted else 0)

        except intcode.Halted:
            break

    return painted, len(painted_ever)


painted, num_painted = run_robot(instructions, 0)
print(num_painted)

painted, num_painted = run_robot(instructions, 1)

# Now we just draw painted
bottom_left = (min(pos[0] for pos in painted), min(pos[1] for pos in painted))
top_right = (max(pos[0] for pos in painted), max(pos[1] for pos in painted))

for y in range(top_right[1], bottom_left[1] - 1, -1):
    row = []
    for x in range(bottom_left[0], top_right[0] + 1):
        row.append("█" if (x, y) in painted else " ")
    print("".join(row))
