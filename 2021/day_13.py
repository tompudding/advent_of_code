import sys


class FoldDirection:
    Horizontal = 0
    Vertical = 1


class Paper:
    def __init__(self, lines):
        blank = lines.index("\n")
        dots_text, folds_text = lines[:blank], lines[blank + 1 :]

        self.dots = []
        self.folds = []

        self.width = 0
        self.height = 0

        self.fold_funcs = {
            FoldDirection.Horizontal: self.fold_horizontal,
            FoldDirection.Vertical: self.fold_vertical,
        }

        for dot_text in dots_text:
            x, y = (int(n) for n in dot_text.strip().split(","))

            if x >= self.width:
                self.width = x + 1
            if y >= self.height:
                self.height = y + 1

            self.dots.append((x, y))

        for fold_text in folds_text:
            fold = fold_text.strip().split("fold along ")[1]

            n = int(fold.split("=")[1])

            if fold[0] == "x":
                self.folds.append((FoldDirection.Vertical, n))
            else:
                self.folds.append((FoldDirection.Horizontal, n))

        self.grid = [[0 for row in range(self.height)] for col in range(self.width)]

        for x, y in self.dots:
            self.grid[x][y] = 1

    def perform_fold(self, num):
        for i in range(num):
            fold_dir, pos = self.folds.pop(0)

            self.fold_funcs[fold_dir](pos)

        return len(self.folds)

    def fold_horizontal(self, split_row):
        # For each column, we want to fold the bottom into the top and cut it

        for col in range(self.width):
            for row in range(1, self.height + 1 - (split_row + 1)):
                self.grid[col][split_row - row] |= self.grid[col][split_row + row]

            # then we don't need the rest
            self.grid[col] = self.grid[col][:split_row]

        self.height = split_row

    def fold_vertical(self, split_col):
        # We just want to fold some columns into some others
        for col in range(1, self.width + 1 - (split_col + 1)):
            # we're merging col split_col + col with split_col - col

            for row in range(self.height):
                self.grid[split_col - col][row] |= self.grid[split_col + col][row]

        self.grid = self.grid[:split_col]

        self.width = split_col

    def count_dots(self):
        total = 0
        for col in range(self.width):
            total += sum(self.grid[col])
        return total

    def __repr__(self):
        out = []
        for y in range(self.height):
            out.append("".join(("█" if self.grid[x][y] else " " for x in range(self.width))))
        return "\n".join(out)


with open(sys.argv[1], "r") as file:
    lines = file.readlines()


paper = Paper(lines)

paper.perform_fold(1)

print(paper.count_dots())

paper.perform_fold(len(paper.folds))

print(paper)
