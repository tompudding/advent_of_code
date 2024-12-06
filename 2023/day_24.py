import sys
import math
from fractions import Fraction


class Trajectory:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

        # Put it into the form y = ax + b for t = 0
        #
        # we have x = vel[0]*t + pos[0]
        #         y = vel[1]*t + pos[1]

        # (x - pos[0])/vel[0] = (y - pos[1])/vel[1]
        #
        # y - pos[1] = vel[1]*(x - pos[0])/vel[0]
        # y = vel[1]*(x - pos[0])/vel[0] + pos[1]
        # y = vel[1]/vel[0]*x - vel[1]/vel[0]*pos[0] + pos[1]
        self.a = Fraction(numerator=self.vel[1], denominator=self.vel[0])
        self.b = self.pos[1] - self.a * self.pos[0]

        # for fun we also consider the other direction and the x/z line
        self.za = Fraction(numerator=self.vel[2], denominator=self.vel[0])
        self.zb = self.pos[2] - self.za * self.pos[0]

    def get_time(self, x, y):
        return Fraction((x - self.pos[0]), self.vel[0])

    def adjust(self, delta_v):
        return Trajectory(
            self.pos, (self.vel[0] + delta_v[0], self.vel[1] + delta_v[1], self.vel[2] + delta_v[2])
        )

    def intersect(self, other, need_positive=True):
        # ax + b = a1x + b1
        # ax - a1x = b1 - b
        # x = (b1 - b) / (a - a1)
        try:
            x = Fraction((other.b - self.b), (self.a - other.a))
            y = self.a * x + self.b
        except ZeroDivisionError:
            # parallel
            return None

        if not need_positive:
            return x, y

        # We're only interested in things in the future
        times = (traj.get_time(x, y) for traj in [self, other])

        if any(t < 0 for t in times):
            return None

        return (x, y)

    def zintersect(self, other):
        try:
            x = Fraction((other.zb - self.zb), (self.za - other.za))
            z = self.za * x + self.zb
        except ZeroDivisionError:
            return None

        return x, z

    def __repr__(self):
        return f"{self.pos=} {self.vel=} {self.a=} {self.b=}"


class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def intersect(self, other):
        try:
            x = Fraction((other.b - self.b), (self.a - other.a))
            y = self.a * x + self.b
        except ZeroDivisionError:
            return None

        return x, y


with open(sys.argv[1], "r") as file:
    trajectories = []
    for line in file:
        line = line.strip()
        pos, vel = line.split("@")
        pos = [int(part) for part in pos.split(",")]
        vel = [int(part) for part in vel.split(",")]

        trajectories.append(Trajectory(pos, vel))


def test_bounds(lowest, highest):
    count = 0

    for i, a in enumerate(trajectories):
        for j in range(i + 1, len(trajectories)):
            b = trajectories[j]
            intersect = a.intersect(b)
            if intersect is None:
                continue
            if all(lowest <= coord <= highest for coord in a.intersect(b)):
                count += 1

    return count


print(test_bounds(200000000000000, 400000000000000))


# x = t*vel + pos
# x = t*vel1 + pos1
# pos1 = t(vel - vel1) + pos

# For part 2 let's take each dimension independently, and assume a velocity for the throw line.
# Then we can look at each existing line and form a new "line" in t with ratio of the difference of the line's velocity and our assumed velocity. This line must intersect the other lines at the same place, our starting position.

lines = []
possible_xy = []
lim = 16384
vel_x = 0
incrementor = 0


def is_integer(x):
    return x.denominator == 1


def is_integer_point(point):
    return point and is_integer(point[0]) and is_integer(point[1])


def test_trajectories(trajectories, pos, vel):
    print(pos)
    print(vel)
    guess = Trajectory(pos, vel)

    times = []
    for i, line in enumerate(trajectories):
        pos = line.intersect(guess, need_positive=False)
        if pos is None:
            print("No intersection at all!")
            return False
        t = guess.get_time(*pos)
        print(i, t)
        if not is_integer(t):
            return False

    return True


lim = 300
for vel_x in range(-lim, lim):
    # new_traj = [traj.adjust((-vel_x, -vel_y, 0)) for traj in trajectories]
    for vel_y in range(-lim, lim):
        adj = (-vel_x, -vel_y, 0)
        intersection = None
        match = None

        for i in range(len(trajectories) - 1):
            try:
                a = trajectories[i].adjust(adj)
                b = trajectories[i + 1].adjust(adj)
            except ZeroDivisionError:
                break

            x = a.intersect(b, need_positive=False)

            if x is None:
                continue

            if not is_integer_point(x):
                # print(f"reject {vel_x} {vel_y} due to non integer {x}")
                break

            # This seems good
            match = x
            break
        if match is None:
            continue

        # print("A", x)

        # Try that for z-ness
        for vel_z in range(-lim, lim):
            adj = (-vel_x, -vel_y, -vel_z)
            for i in range(len(trajectories) - 1):
                try:
                    a = trajectories[i].adjust(adj)
                    b = trajectories[i + 1].adjust(adj)
                except ZeroDivisionError:
                    continue

                x = a.zintersect(b)

                if x is None:
                    continue

                if not is_integer_point(x):
                    break

                if x[0] != match[0]:
                    # print("no go", x, match[0])
                    break

                # This seems good
                # print("B", vel_x, vel_y, vel_z, x)
                pos = (match[0], match[1], x[1])
                vel = (vel_x, vel_y, vel_z)

                if test_trajectories(trajectories, pos, vel):
                    print("Bingo", pos, sum(pos))
                    quit()
                break
