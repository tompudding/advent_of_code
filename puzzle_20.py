import sys


class Image:
    def __init__(self, outside):
        self.pixels = {}
        self.aggregate = {}
        self.min = [0, 0]
        self.max = [0, 0]
        self.outside = outside
        # print(f"{outside=}")

    def set_pixel(self, x, y):
        self.pixels[x, y] = 1

        for pos, index in ((x, 0), (y, 1)):
            if pos < self.min[index]:
                self.min[index] = pos
            if pos > self.max[index]:
                self.max[index] = pos

    def expand(self):
        # The outside will flip if the first bit in the lookup is set
        new = Image(
            self.outside ^ lookup[0],
        )

        for x in range(self.min[0] - 1, self.max[0] + 2):
            for y in range(self.min[1] - 1, self.max[1] + 2):
                pixel_data = 0
                shift = 0
                for delta_y in (1, 0, -1):
                    for delta_x in (1, 0, -1):
                        pos = x + delta_x, y + delta_y
                        bit = 0
                        if pos in self.pixels:
                            bit = 1
                        elif self.outside and (
                            pos[0] < self.min[0]
                            or pos[0] > self.max[0]
                            or pos[1] < self.min[1]
                            or pos[1] > self.max[1]
                        ):
                            bit = 1

                        pixel_data |= bit << shift
                        shift += 1
                # print(f"{x=} {y=} {pixel_data=:x}")

                if lookup[pixel_data]:
                    new.set_pixel(x, y)

        return new

    def count_bits(self):
        # print(f"{len(self.pixels)=} {len(self.aggregate)=}")
        if self.outside:
            # There are infinite set bits
            return 0
        return len(self.pixels)

    def __repr__(self):
        out = []

        for y in range(self.min[1], self.max[1] + 1):
            out.append(
                "".join(
                    ("#" if self.pixels.get((x, y), 0) else "." for x in range(self.min[0], self.max[0] + 1))
                )
            )
        return "\n".join(out)


image = Image(outside=0)

with open(sys.argv[1], "r") as file:
    lookup = [1 if char == "#" else 0 for char in file.readline().strip()]
    file.readline()
    for y, line in enumerate(file):
        print(y, line.strip())
        for x, bit in enumerate(line.strip()):
            if bit == "#":
                image.set_pixel(x, y)

print(image)
print("-" * 10)

for step in range(50):
    image = image.expand()
    # print(image)
    print(image.count_bits())
    # print(f"{image.min=} {image.max=}")
