import sys
import intcode
import os
import time


class TileID:
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4

    icons = {EMPTY: " ", WALL: "█", BLOCK: "#", HORIZONTAL_PADDLE: "-", BALL: "o"}


width = 36
height = 23


def draw(screen, score):
    os.system("clear")
    if not screen:
        return

    out = []

    for row in range(height):
        row_icons = []
        for col in range(width):
            try:
                icon = TileID.icons[screen[(col, row)]]
            except KeyError:
                icon = " "
            row_icons.append(icon)
        out.append("".join(row_icons))

    print("\n".join(out))
    print("SCORE : ", score)
    print("-" * 30)
    # time.sleep(1 / 30)


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])


program = intcode.IntCode(instructions, [])
program.run()

screen = {}


for pos in range(0, len(program.output), 3):
    x, y, id = program.output[pos : pos + 3]

    screen[x, y] = id

print(len([id for id in screen.values() if id == TileID.BLOCK]))

# Part 2
program = intcode.IntCode(instructions, [])
program.set_memory(0, [2])
num_inputs = 0
screen = {}
ball_pos = paddle_pos = None

while not program.halted:
    try:
        program.resume()
    except intcode.InputStall:
        num_inputs += 1

        for pos in range(0, len(program.output), 3):
            x, y, id = program.output[pos : pos + 3]

            if (x, y) == (-1, 0):
                score = id
                # print("New score", score)
                continue

            if id == TileID.BALL:
                ball_pos = (x, y)
            elif id == TileID.HORIZONTAL_PADDLE:
                paddle_pos = (x, y)

            if id == 0:
                if (x, y) in screen:
                    del screen[x, y]
            else:
                screen[x, y] = id

        # draw(screen, score)

        joystick = 0

        if ball_pos[0] < paddle_pos[0]:
            joystick = -1
        elif ball_pos[0] > paddle_pos[0]:
            joystick = 1
        # print(ball_pos[0], paddle_pos[0], joystick)

        program.inputs.append(joystick)
        program.output = []
    except intcode.Halted:
        pass

for pos in range(0, len(program.output), 3):
    x, y, id = program.output[pos : pos + 3]

    if (x, y) == (-1, 0):
        score = id
        # print("New score", score)
        continue
print(score)
