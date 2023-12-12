import sys


class Impossible(Exception):
    pass


def get_runs(array):
    runs = []

    current = 0
    on_run = None
    for i, char in enumerate(array):
        if char == "#":
            if on_run is None:
                on_run = i
            current += 1
            continue
        else:
            if on_run is not None:
                runs.append((on_run, current))
                current = 0
                on_run = None
    if on_run is not None:
        runs.append((on_run, current))

    return sorted(runs, key=lambda x: -x[1])


class SpringRow:
    def __init__(self, springs, groups):
        # Firstly we can ignore any leading or trailing dots
        self.springs = [spring for spring in springs.split(".") if spring]

        # We can also replace any repeated dots with a single dot
        self.groups = groups

        self.orig_springs = [spring for spring in self.springs]
        self.orig_groups = [group for group in self.groups]

        # print("New spring:", self)

        try:
            self.simplify()
        except:
            # Here we just assume it's impossible
            self.groups = []
            self.springs = [""]
            # print("SIMPLIFICATION ERROR:")
            # print(self)

        # print("Simplified to:", self)

        self.question_marks = sum(spring.count("?") for spring in self.springs)

    def is_bad(self):
        # We can do a very basic test here. Are there too many #s for our groups?
        hashes = sum(spring.count("#") for spring in self.springs)

        if hashes > sum(self.groups):
            return True

        # What if the longest run is already too long?
        working = [c for c in ".".join(self.springs)]
        runs = get_runs(working)

        if runs and all(runs[0][1] > group for group in self.groups):
            return True

        return False

    def simplify(self):
        # Start by inferring everything we can

        if not self.groups:
            return

        current_spring = 0
        modified = True

        while modified and self.springs:
            modified = False
            # print("A", self)
            # for end_group in range(1, len(self.groups)):
            #     if len(self.springs[0]) == sum(group for group in self.groups[:end_group]) + (end_group - 1):
            #         # There is only one way to achieve this so we can ignore it
            #         self.springs = self.springs[1:]
            #         self.groups = self.groups[end_group:]
            #         modified = True
            #         break
            # print("B", self)

            # # Also go from the other end
            # for end_group in range(len(self.groups) - 1, -1, -1):
            #     if len(self.springs[-1]) == sum(group for group in self.groups[end_group:]) + (
            #         len(self.groups) - end_group - 1
            #     ):
            #         # There is only one way to achieve this so we can ignore it
            #         self.springs = self.springs[:-1]
            #         self.groups = self.groups[:end_group]
            #         modified = True
            #         break

            # print("B.5", self)
            # if self.is_bad():
            #     raise Impossible

            self.springs = [spring for spring in self.springs if spring]
            if not self.springs:
                break

            # print("C", self)

            # If the first or last springs start with a hash, we know how many hashes there must be and we can eat those
            if self.springs[0].startswith("#"):
                if len(self.springs[0]) < self.groups[0]:
                    raise Impossible

                self.springs[0] = self.springs[0][self.groups[0] :]

                if self.springs[0]:
                    if self.springs[0][0] == "#":
                        raise Impossible
                    self.springs[0] = self.springs[0][1:]

                self.groups = self.groups[1:]
                self.springs = [spring for spring in self.springs if spring]
                modified = True
                # print("C.5", self)
                continue

            # print("D", self)

            if self.springs[-1].endswith("#"):
                # We're going to trip a bunch of #s from the end, but if there are any left they must end in a
                # question mark and we now know that question mark which we can remove as it must be a dot
                if len(self.springs[-1]) < self.groups[-1]:
                    raise Impossible

                self.springs[-1] = self.springs[-1][: -(self.groups[-1])]

                if self.springs[-1]:
                    if self.springs[-1][-1] == "#":
                        raise Impossible
                    self.springs[-1] = self.springs[-1][:-1]

                self.groups = self.groups[:-1]
                self.springs = [spring for spring in self.springs if spring]
                modified = True
                continue

            # print("E", self)

            # We can check the first question mark and see if it must be one or the other
            if self.springs[0][0] == "?":
                # How many hashes are there after this
                try:
                    idx = self.springs[0].index("?", 1)
                except ValueError:
                    idx = len(self.springs[0])

                # print("BONK", idx)

                if idx > 1:
                    if idx - 1 == self.groups[0]:
                        self.springs[0] = self.springs[0][1:]
                        modified = True
                        continue

    def match(self):
        working = [c for c in ".".join(self.springs)]

        runs = []
        current = 0
        on_run = False
        for char in working:
            if char == "#":
                on_run = True
                current += 1
                continue
            else:
                if on_run:
                    runs.append(current)
                    current = 0
                    on_run = False
        if on_run:
            runs.append(current)

        # print("amongo", working, runs, groups)

        return 1 if runs == self.groups else 0

    def get_num_arrangements(self):
        if not self.springs:
            # This is the degenerate case
            if self.groups:
                # print("ZEro")
                return 0
            # print("ONE")
            return 1
        if not self.groups:
            # This is valid if all the springs are empty
            if set("".join(self.springs)) == {"?"}:
                return 1
            # print("Zero")
            return 0

        # Handle a simple case: n ? and one group of m means there are n - m + 1 ways
        working = [c for c in ".".join(self.springs)]

        if len(self.groups) == 1 and set(working) == {"?"}:
            return len(working) - self.groups[0] + 1
        # print("W", working)

        # We want to start at the position most likely to make an invalid arrangement soonest, so let's go
        # with the one that makes the longest run
        idx = None

        # runs = get_runs(working)
        # for pos, length in runs:
        #     if pos > 0 and working[pos - 1] == "?":
        #         idx = pos - 1
        #         break
        #     elif pos + length < len(working) and working[pos + length] == "?":
        #         idx = pos + length
        #         break

        if idx is None:
            try:
                idx = working.index("?")
            except ValueError:
                return self.match()
        # else:
        # print(f"selected idx {idx} for", working)

        a = SpringRow("".join(working[:idx] + ["#"] + working[idx + 1 :]), self.groups).get_num_arrangements()
        b = SpringRow("".join(working[:idx] + ["."] + working[idx + 1 :]), self.groups).get_num_arrangements()

        # print("AB", working, a, b)
        return a + b

    def __repr__(self):
        spring_string = ".".join(spring for spring in self.springs)
        group_string = ",".join((str(group) for group in self.groups))
        return f"{self.springs} {group_string} ({self.orig_springs} {self.orig_groups})"


rows = []

with open(sys.argv[1], "r") as file:
    for line in file:
        springs, groups = line.strip().split()
        groups = [int(group) for group in groups.split(",")]
        rows.append(SpringRow(springs, groups))


# print(sum(2**row.question_marks for row in rows))
total = 0
for row in rows:
    # print(row)
    num = row.get_num_arrangements()
    # print("**", row, num)
    total += num

print(total)

rows = []

with open(sys.argv[1], "r") as file:
    for line in file:
        springs, groups = line.strip().split()
        springs = "?".join([springs] * 5)
        groups = ",".join([groups] * 5)
        groups = [int(group) for group in groups.split(",")]
        rows.append(SpringRow(springs, groups))


total = 0
for row in rows:
    # print(row)
    num = row.get_num_arrangements()
    print("**", row, num)
    total += num

print(total)
