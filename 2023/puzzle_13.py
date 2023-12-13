import sys


def test_elems(elems):
    out = []
    for i in range(1, len(elems)):
        for j in range(0, len(elems)):
            try:
                # print("x", elems[i + j] == elems[i - (j + 1)])
                if i - (j + 1) < 0:
                    out.append(i)
                    break
                if elems[i + j] != elems[i - (j + 1)]:
                    break
            except IndexError:
                # print("hello", i)
                out.append(i)
                break
        else:
            out.append(i)

    return out


class Grid:
    def __init__(self, lines):
        self.rows = [line for line in lines]
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.cols = [[row[i] for row in self.rows] for i in range(self.width)]

    def __repr__(self):
        return "\n".join(self.rows)

    def get_mirror_col(self):
        out = test_elems(self.cols)
        if len(out) == 0:
            return 0
        assert len(out) == 1
        return out[0]

    def get_mirror_row(self):
        out = test_elems(self.rows)
        if len(out) == 0:
            return 0
        assert len(out) == 1
        return out[0]


grids = []

with open(sys.argv[1], "r") as file:
    current = []
    for line in file:
        line = line.strip()

        if not line:
            grids.append(Grid(current))
            current = []
            continue

        current.append(line)

    if current:
        grids.append(Grid(current))

for grid in grids:
    print(grid)
    print()

print(sum(grid.get_mirror_col() + 100 * grid.get_mirror_row() for grid in grids))
