import sys

class Node:
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.children = {}
        self.size = 0

    def get_child(self, name):
        raise ValueError

    def get_size(self):
        return self.size

class Dir(Node):
    def get_child(self, name):
        if name == '..':
            return self.parent
        return self.children[name]

    def add_child(self, node):
        self.children[node.name] = node

    def get_size(self):
        if self.size == 0:
            self.size = sum(child.get_size() for child in self.children.values())
        return self.size

class File(Node):
    def __init__(self, name, parent, size):
        super().__init__(name, parent)
        self.size = int(size)

root = Dir('/', None)
all_dirs = [root]
pwd = root
listing = None

with open(sys.argv[1], 'r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('$ '):
            listing = None
            # This is a command
            line = line[2:]
            try:
                cmd, arg = line.split()
            except ValueError:
                cmd = line
                arg = ''
            if cmd == 'ls':
                listing = pwd
                continue
            elif cmd == 'cd':
                if arg == '/':
                    pwd = root
                    continue
                pwd = pwd.get_child(arg)
                continue
        elif listing:
            size, name = line.split()
            if size == 'dir':
                node = Dir(name, pwd)
                all_dirs.append(node)
            else:
                node = File(name, pwd, size)
            pwd.add_child(node)

#Part 1
total = 0
for dir in all_dirs:
    size = dir.get_size()
    if size > 100000:
        continue
    total += size

print(total)

#Part 2

disk_size = 70000000
needed = 30000000

free = disk_size - root.get_size()
to_delete = needed - free
print(free)

best = disk_size
for dir in all_dirs:
    size = dir.get_size()
    if size >= to_delete and size < best:
        best = size

print(best)
