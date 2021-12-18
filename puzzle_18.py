import sys
import copy


class SnailfishNumber:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.parent = None

        for child in self.a, self.b:
            if isinstance(child, SnailfishNumber):
                child.set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def depth(self):
        depth = 0
        parent = self.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth

    def __add__(self, other):
        new = SnailfishNumber(self, other)
        new.reduce()

        return new

    def __repr__(self):
        return f"[{self.a},{self.b}]"

    # def __iadd__

    def reduce(self):
        # print("start reduce", self)
        while True:
            # Check if anything needs to explode
            if isinstance(self.a, SnailfishNumber) and self.a.explode():
                # print("left explode", self)
                continue

            if isinstance(self.b, SnailfishNumber) and self.b.explode():
                # print("right explode", self)
                continue

            # No explodes, so maybe there's a split?
            # ...
            if isinstance(self.a, SnailfishNumber) and self.a.split():
                # print("left split", self)
                continue

            if isinstance(self.b, SnailfishNumber) and self.b.split():
                # print("right split", self)
                continue

            # Nothing happened so we're done
            break

    def split(self):
        for child in self.a, self.b:
            if isinstance(child, SnailfishNumber):
                if child.split():
                    return True
            elif child > 9:
                smaller = child // 2
                new = SnailfishNumber(smaller, child - smaller)
                new.set_parent(self)

                if child is self.a:
                    self.a = new
                else:
                    self.b = new

                return True

    def both_numbers(self):
        return not isinstance(self.a, SnailfishNumber) and not isinstance(self.b, SnailfishNumber)

    def add_to_leftmost(self, num_to_add):
        num = self
        while isinstance(num, SnailfishNumber):
            last = num
            num = num.a

        last.a += num_to_add

    def add_to_rightmost(self, num_to_add):
        num = self
        while isinstance(num, SnailfishNumber):
            last = num
            num = num.b

        last.b += num_to_add

    def explode(self):
        for child in self.a, self.b:
            if isinstance(child, SnailfishNumber):
                if child.both_numbers():
                    if child.depth() >= 4:
                        # we need to get the next left-most number which can be a little tricky. We follow the tree
                        # upwards and stop when we're the right branch. If we're always the left branch, there is nothing
                        # to our left
                        # print("hello", child)
                        left = None
                        num = child
                        while num:
                            parent = num.parent
                            if parent and num is parent.b:
                                # Aha,
                                left = parent.a
                                if isinstance(parent.a, SnailfishNumber):
                                    parent.a.add_to_rightmost(child.a)
                                else:
                                    parent.a += child.a

                                break
                            num = parent
                        # Now we have to find the right
                        num = child
                        while num:
                            parent = num.parent
                            if parent and num is parent.a:
                                # Aha,
                                # print("yoyo", parent.b, child.b)
                                if isinstance(parent.b, SnailfishNumber):
                                    parent.b.add_to_leftmost(child.b)
                                else:
                                    parent.b += child.b

                                break
                            num = parent
                        if child is self.a:
                            self.a = 0
                        else:
                            self.b = 0
                        # This exploded
                        return True

                else:
                    if child.explode():
                        return True
        return False

    def magnitude(self):

        magnitudes = [
            child.magnitude() if isinstance(child, SnailfishNumber) else child for child in (self.a, self.b)
        ]

        return 3 * magnitudes[0] + 2 * magnitudes[1]


def number_factory(line):
    # Let's get crazy
    line = line.replace("[", "SnailfishNumber(")
    line = line.replace("]", ")")
    return eval(line)


total = None
numbers = []
with open(sys.argv[1], "r") as file:
    for line in file:
        num = number_factory(line.strip())
        numbers.append(copy.deepcopy(num))
        if total is None:
            total = num
        else:
            total += num


print(total.magnitude())


# I'm sure there's a clever way to approach part 2, but part 1 was enough of a shitshow
max_mag = 0

for number in numbers:
    for other in numbers:
        if number is other:
            continue
        total = (copy.deepcopy(number) + copy.deepcopy(other)).magnitude()
        if total > max_mag:
            max_mag = total
print(max_mag)
