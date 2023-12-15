import sys


def hash_func(x):
    total = 0

    for char in x:
        total = ((total + ord(char)) * 17) & 0xFF

    # print(x, total)
    return total


class Box:
    def __init__(self, box_num):
        self.lenses = []
        self.num = box_num
        self.in_box = {}

    def add_lense(self, new_lense):
        try:
            self.in_box[new_lense].focal_length = new_lense.focal_length
        except KeyError:
            self.lenses.insert(0, new_lense)
            self.in_box[new_lense] = new_lense

    def remove_lense(self, new_lense):
        if new_lense not in self.in_box:
            return

        self.lenses.remove(new_lense)
        del self.in_box[new_lense]

    def focusing_power(self):
        total = 0

        for i, lense in enumerate(reversed(self.lenses)):
            total += (self.num + 1) * (i + 1) * int(lense.focal_length)

        return total

    def __repr__(self):
        out = [f"Box {self.num:}"]

        for lense in reversed(self.lenses):
            out.append(repr(lense))

        return " ".join(out)


class Lense:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        return self.label == other.label

    def __repr__(self):
        return f"[{self.label} {self.focal_length}]"


class Item:
    def __init__(self, text, boxes):
        self.text = text
        self.boxes = boxes
        if "=" in text:
            self.label, self.focal_length = text.split("=")
            self.op = self.add
        else:
            self.label, self.focal_length = text.split("-")
            self.op = self.remove

        self.box = hash_func(self.label)

    def add(self):
        boxes[self.box].add_lense(Lense(self.label, self.focal_length))

    def remove(self):
        boxes[self.box].remove_lense(Lense(self.label, self.focal_length))


boxes = [Box(i) for i in range(256)]


total = 0
init_sequence = []
with open(sys.argv[1], "r") as file:
    for line in file:
        for item in line.strip().split(","):
            init_sequence.append(Item(item, boxes))
            total += hash_func(item)


print(total)

for item in init_sequence:
    item.op()

#     print(f"After {item.text}")

#     for box in boxes:
#         if not box.lenses:
#             continue
#         print(box)

print(sum(box.focusing_power() for box in boxes))
