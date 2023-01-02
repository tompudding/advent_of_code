#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class Layer:
    def __init__(self, width, height, txt):
        self.txt = txt[: width * height]
        self.counts = {0: 0, 1: 0, 2: 0}
        self.width = width
        self.height = height
        for char in self.txt:
            char = int(char)
            try:
                self.counts[char] += 1
            except KeyError:
                self.counts[char] = 1


class Colours:
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


pixel_map = {0: " ", 1: "█", 2: "c"}


def get_pixel(layers, pos):
    pos = (pos[1] * layers[0].width) + pos[0]
    for i in range(len(layers)):
        pixel = int(layers[i].txt[pos])
        if pixel == Colours.TRANSPARENT:
            continue

        return pixel_map[pixel]


width = 25
height = 6
with open(sys.argv[1], "r") as file:
    txt = file.read().strip()
    layers = [
        Layer(width, height, txt[pos : pos + width * height]) for pos in range(0, len(txt), width * height)
    ]

sorted_layers = sorted(layers, key=lambda x: x.counts[0])

print(sorted_layers[0].counts[1] * sorted_layers[0].counts[2])

for row in range(height):
    line = []
    for col in range(width):
        pixel = get_pixel(layers, (col, row))
        line.append(pixel)
    print("".join(line))
