import sys
import math
from fractions import Fraction


class Trajectory:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel


with open(sys.argv[1], "r") as file:
    trajectories = []
    for line in file:
        line = line.strip()
        pos, vel = line.split("@")
        pos = [int(part) for part in pos.split(",")]
        vel = [int(part) for part in vel.split(",")]

        trajectories.append(Trajectory(pos, vel))

# Try doing x first

x_vels = set(traj.vel[0] for traj in trajectories)

possible = None

for vel_x in range(63, 64):
    # p_r + v_r * t_n = c_n

    # p_0 + v_0 * t_0 = c_0

    # p_0 + v_n * t_n = p_r + v_r * t_n

    # p_n + t_n(v_n - v_r) = p_r

    # So v_n - v_r must divide p_r - p_n, i.e possibilities for p_r can be found by multiplying v_n-v_r up and subtracting p_n.
    # if vel_x in x_vels:
    #    print("Nope")
    #    continue

    # print(f"consider {vel_x=}")

    for traj in trajectories:
        possible_pos_x = {i * (traj.vel[0] - vel_x) + traj.pos[0] for i in range(16384)}

        if possible is None:
            possible = possible_pos_x
        else:
            possible &= possible_pos_x

        print(len(possible))
        if not possible:
            break

    if possible:
        print(vel_x)
        print(len(possible))
        break
