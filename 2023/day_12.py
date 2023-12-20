import sys


class Impossible(Exception):
    pass


cache = {}


class SpringRow:
    def __init__(self, springs, groups):
        # Firstly we can ignore any leading or trailing dots
        self.springs = [spring for spring in springs.split(".") if spring]

        # We can also replace any repeated dots with a single dot
        self.groups = groups

        self.orig_springs = [spring for spring in self.springs]
        self.orig_groups = [group for group in self.groups]

        try:
            self.simplify()
        except Impossible:
            # Here we just assume it's impossible
            self.groups = []
            self.springs = [""]

        self.question_marks = sum(spring.count("?") for spring in self.springs)

    def simplify(self):
        # Start by inferring everything we can

        if not self.groups:
            return

        current_spring = 0
        modified = True

        while modified and self.springs:
            modified = False

            if len(self.groups) == 0 and any("#" in spring for spring in self.springs):
                raise Impossible

            self.springs = [spring for spring in self.springs if spring]
            if not self.springs:
                break

            # If the first or last springs start with a hash, we know how many hashes there must be and we can eat those
            if self.springs[0].startswith("#"):
                if len(self.springs[0]) < self.groups[0]:
                    raise Impossible

                self.springs[0] = self.springs[0][self.groups[0] :]

                if self.springs[0]:
                    if self.springs[0].startswith("#"):
                        raise Impossible
                    self.springs[0] = self.springs[0][1:]

                self.groups = self.groups[1:]
                self.springs = [spring for spring in self.springs if spring]
                modified = True

                continue

            if self.springs[-1].endswith("#"):
                # We're going to trip a bunch of #s from the end, but if there are any left they must end in a
                # question mark and we now know that question mark which we can remove as it must be a dot

                if len(self.springs[-1]) < self.groups[-1]:
                    raise Impossible

                self.springs[-1] = self.springs[-1][: -(self.groups[-1])]

                if self.springs[-1]:
                    if self.springs[-1].endswith("#"):
                        raise Impossible
                    self.springs[-1] = self.springs[-1][:-1]

                self.groups = self.groups[:-1]
                self.springs = [spring for spring in self.springs if spring]
                modified = True
                continue

            # We can check the first question mark and see if it must be one or the other
            if self.springs[0][0] == "?":
                # How many hashes are there after this
                try:
                    idx = self.springs[0].index("?", 1)
                except ValueError:
                    idx = len(self.springs[0])

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

        return 1 if runs == self.groups else 0

    def get_num_arrangements(self):
        if not self.springs:
            # This is the degenerate case
            if self.groups:
                return 0

            return 1
        if not self.groups:
            # This is valid if all the springs are empty
            if set("".join(self.springs)) == {"?"}:
                return 1

            return 0

        # Handle a simple case: n ? and one group of m means there are n - m + 1 ways
        working = [c for c in ".".join(self.springs)]
        key = tuple(working), tuple(self.groups)
        try:
            return cache[key]
        except KeyError:
            pass

        if len(self.groups) == 1 and set(working) == {"?"} and len(working) >= self.groups[0]:
            final = len(working) - self.groups[0] + 1
            cache[key] = final
            return final

        try:
            idx = working.index("?")
        except ValueError:
            return self.match()

        a = SpringRow("".join(working[:idx] + ["#"] + working[idx + 1 :]), self.groups).get_num_arrangements()
        b = SpringRow("".join(working[:idx] + ["."] + working[idx + 1 :]), self.groups).get_num_arrangements()

        return a + b

    def __repr__(self):
        spring_string = ".".join(spring for spring in self.springs)
        group_string = ",".join((str(group) for group in self.groups))
        return f"{self.springs} {group_string} ({self.orig_springs} {self.orig_groups})"


rows = []

with open(sys.argv[1], "r") as file:
    lines = [line.strip().split() for line in file]


rows = [SpringRow(springs, [int(group) for group in groups.split(",")]) for springs, groups in lines]


print(sum(row.get_num_arrangements() for row in rows))

rows = []
for springs, groups in lines:
    springs = "?".join([springs] * 5)
    groups = ",".join([groups] * 5)
    groups = [int(group) for group in groups.split(",")]
    rows.append(SpringRow(springs, groups))

print(sum(row.get_num_arrangements() for row in rows))
