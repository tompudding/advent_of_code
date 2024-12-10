import sys

# This is horrific but it gives the right answer

with open(sys.argv[1], "r") as file:
    data = file.read().strip()

files = []
space = []

block = 0
pos = 0
for data_pos in range(0, len(data), 2):
    try:
        file_length, space_length = (int(v) for v in data[data_pos : data_pos + 2])
    except ValueError:
        file_length = int(data[data_pos])
        space_length = 0
    files.append((block, pos, file_length))
    if space_length:
        space.append([pos + file_length, space_length])
    block += 1
    pos += file_length + space_length

# Build the whole thing?
disk_len = pos
disk = [None for i in range(disk_len)]

for block_id, file_pos, file_length in files:
    for x in range(file_length):
        disk[file_pos + x] = block_id

pos = 0
for block_id, file_pos, file_length in reversed(files):
    for x in range(file_length):
        while disk[pos] is not None:
            pos += 1

        if file_pos + x <= pos:
            break
        disk[pos] = block_id
        disk[file_pos + x] = None
        # print(f"putting {block_id} at {pos} {file_pos + x}")
        pos += 1

# print(disk)
total = 0
for i, val in enumerate(disk):
    if val is None:
        continue
    total += i * val

print(total)


def compute_free_space(disk):
    in_free = False
    in_pos = 0
    out = []
    for pos, val in enumerate(disk):
        if in_free:
            if val is None:
                free_len += 1
            else:
                out.append((in_pos, free_len))
                in_free = False
        else:
            if val is None:
                in_free = True
                in_pos = pos
                free_len = 1

    if in_free:
        out.append((in_pos, free_len))
    return out


disk = [None for i in range(disk_len)]

for block_id, file_pos, file_length in files:
    for x in range(file_length):
        disk[file_pos + x] = block_id

# print(space)


for block_id, file_pos, file_length in reversed(files):
    placed = None
    for free_pos, free_len in space:
        if free_len >= file_length and free_pos < file_pos:
            for x in range(file_length):
                disk[free_pos + x] = block_id
                disk[file_pos + x] = None
            placed = free_pos
            break
    if placed is not None:
        # We should at least update just the parts of this that have changed, but this problem is tedious
        space = compute_free_space(disk)

# print(disk)

total = 0
for i, val in enumerate(disk):
    if val is None:
        continue
    total += i * val

print(total)
