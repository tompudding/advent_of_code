import sys

def item_priority(item):
    if 'a' <= item <= 'z':
        return ord(item)-ord('a')+1
    else:
        return ord(item)-ord('A')+27

data = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()
        mid = len(line)//2
        compartments = [set(line[:mid]),set(line[mid:])]
        data.append(compartments)

score = 0
for compartments in data:
    common = compartments[0] & compartments[1]
    if len(common) != 1:
        raise ValueError(compartments)
    score += item_priority(common.pop())

print(score)

score = 0
for pos in range(0, len(data), 3):
    comp = data[pos:pos+3]
    common = comp[0][0] | comp[0][1]
    for backpack in comp[1:]:
        common &= (backpack[0] | backpack[1])
    if len(common) != 1:
        raise ValueError(comp)
    score += item_priority(common.pop())

print(score)
