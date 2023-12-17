import sys


def test_elems(elems):
    out = []
    for i in range(1, len(elems)):
        for j in range(0, len(elems)):
            try:
                if i - (j + 1) < 0:
                    out.append(i)
                    break
                if elems[i + j] != elems[i - (j + 1)]:
                    break
            except IndexError:
                out.append(i)
                break
        else:
            out.append(i)

    return out


class Grid:
    def __init__(self, lines):
        self.rows = [list(line) for line in lines]
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.cols = [[row[i] for row in self.rows] for i in range(self.width)]

        self.base_cols = test_elems(self.cols)
        self.base_rows = test_elems(self.rows)

        if self.base_cols and self.base_rows:
            raise IOnlyExpectedTheOneMirror

    def __repr__(self):
        return "\n".join("".join(row) for row in self.rows)

    def get_mirror_col(self):
        out = self.base_cols
        if len(out) == 0:
            return 0
        assert len(out) == 1
        return out[0]

    def get_mirror_row(self):
        out = self.base_rows
        if len(out) == 0:
            return 0
        assert len(out) == 1
        return out[0]

    def change_selected(self):
        # We try changing every bit and see if it results in a material change to the mirror row or column

        if self.base_cols:
            elems = self.cols
            mirror = self.base_cols
        elif self.base_rows:
            elems = self.rows
            mirror = self.base_rows
        else:
            raise bonk

        for col in range(self.width):
            for row in range(self.height):
                old_item = self.rows[row][col]
                new_item = "." if old_item == "#" else "#"
                self.rows[row][col] = self.cols[col][row] = new_item

                new_rows = test_elems(self.rows)
                new_cols = test_elems(self.cols)

                if new_rows and new_rows != self.base_rows:
                    self.base_rows = [item for item in new_rows if item not in self.base_rows]
                    self.base_cols = []

                    return

                if new_cols and new_cols != self.base_cols:
                    self.base_cols = [item for item in new_cols if item not in self.base_cols]
                    self.base_rows = []
                    return

                self.rows[row][col] = self.cols[col][row] = old_item
        raise NoSmudgeDetected


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

print(sum(grid.get_mirror_col() + 100 * grid.get_mirror_row() for grid in grids))

for grid in grids:
    grid.change_selected()

print(sum(grid.get_mirror_col() + 100 * grid.get_mirror_row() for grid in grids))
