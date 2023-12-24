import sys
import math


def equal(a, b):
    return abs(a[0] - b[0]) < 0.001 and abs(a[1] - b[1]) < 0.001


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
        self.a = self.vel[1] / self.vel[0]
        self.b = self.pos[1] - self.a * self.pos[0]

        # for fun we also consider the other direction and the x/z line
        self.za = self.vel[2] / self.vel[0]
        self.zb = self.pos[2] - self.za * self.pos[0]

    def get_time(self, x, y):
        return (x - self.pos[0]) / self.vel[0]

    def adjust(self, delta_v):
        return Trajectory(
            self.pos, (self.vel[0] + delta_v[0], self.vel[1] + delta_v[1], self.vel[2] + delta_v[2])
        )

    def intersect(self, other, need_positive=True):
        # ax + b = a1x + b1
        # ax - a1x = b1 - b
        # x = (b1 - b) / (a - a1)
        try:
            x = (other.b - self.b) / (self.a - other.a)
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
            x = (other.zb - self.zb) / (self.za - other.za)
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
            x = (other.b - self.b) / (self.a - other.a)
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


def is_integer(point):
    return point is not point[0] % 1.0 < 0.0001 and point[1] % 1.0 < 0.0001


lim = 512
for vel_x in range(-lim, lim):
    # new_traj = [traj.adjust((-vel_x, -vel_y, 0)) for traj in trajectories]
    for vel_y in range(-lim, lim):
        adj = (-vel_x, -vel_y, 0)
        intersection = None
        bad = False

        for i, a in enumerate(trajectories):
            try:
                a_prime = a.adjust(adj)
            except ZeroDivisionError:
                bad = True
                intersection = None
                break

            for j in range(i + 1, len(trajectories)):
                try:
                    b = trajectories[j].adjust(adj)
                    x = a_prime.intersect(b, need_positive=False)
                except ZeroDivisionError:
                    # print(f"reject {vel_x} {vel_y} due to parallel adjusted lines {b} {a.adjust(adj)}")
                    bad = True
                    intersection = None
                    break

                if x is None:
                    continue

                if not is_integer(x):
                    # print(f"reject {vel_x} {vel_y} due to non integer {x}")
                    bad = True
                    intersection = None
                    break

                if intersection is None:
                    intersection = x
                else:
                    if not equal(intersection, x):
                        # print(f"reject {vel_x} {vel_y} due to {intersection} != {x}")
                        bad = True
                        intersection = None
                        break

            # if bad:
            #    break
            break

        if not bad:
            print("why", vel_x, vel_y)
        if intersection:
            possible_xy.append((vel_x, vel_y, intersection))
            print("bingo", vel_x, vel_y, intersection, bad)


# for each of those possibles we can try the range of z values
best = 10 ** 80
for (vel_x, vel_y, (pos_x, pos_y)) in possible_xy:
    for vel_z in range(-10240, 10240):
        adj = (-vel_x, -vel_y, -vel_z)
        for i, a in enumerate(trajectories):
            bad = False
            for j in range(i + 1, len(trajectories)):
                try:
                    b = trajectories[j].adjust(adj)
                    x = a.adjust(adj).zintersect(b)
                except ZeroDivisionError:
                    bad = True
                    break

                if x is None:
                    bad = True
                    break

                if intersection is None:
                    intersection = x
                else:
                    if not equal(intersection, x):
                        bad = True
                        intersection = None
                        break
                    print(intersection, x)

            if bad:
                break

        if intersection and intersection[0] % 1.0 < 0.001 and intersection[1] % 1.0 < 0.001:
            # if int(intersection[0]) == int(pos_x):

            diff = abs(intersection[0] - pos_x)
            if diff <= best:
                best = diff
                print("mingo bingo", vel_x, vel_y, vel_z, pos_x, pos_y, intersection)
                print("diff", diff, "answer", pos_x + pos_y + intersection[1])

            #    print("****")
            #    quit()
