import sys
import intcode
import os
import collections
import heapq
from itertools import chain, combinations


def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))


class Room:
    def __init__(self, cpu):
        data = "".join([chr(c) for c in cpu.output]).strip("\n")
        parts = [part.splitlines() for part in data.split("\n\n")]
        self.name = parts[0][0].strip("=").strip()
        self.description = "n".join(parts[0][1:])
        self.doors = {}
        self.items = []
        self.cpu = cpu.clone()
        self.code = None

        if "Pressure-Sensitive" in self.name:
            # This one is special
            for chunk in parts[1:]:
                for word in chunk:
                    if "ejected" in word:
                        return
                    if "typing " in word:
                        self.code = int(word.split("typing ")[1].split()[0])
                        return

            return
        for chunk in parts[1:]:
            if not chunk:
                continue
            if chunk[0].startswith("Doors"):
                self.doors = {x.strip("-").strip(): None for x in chunk[1:]}
            elif chunk[0].startswith("Items"):
                self.items = {x.strip("-").strip(): None for x in chunk[1:]}

    def take(self, direction, rooms):
        program = self.cpu.clone()
        program.inputs = [ord(c) for c in (direction + "\n")]
        program.output = []
        while True:
            try:
                program.resume()

            except (intcode.Halted, intcode.InputStall):
                pass
            if not program.output:
                continue
            break

        assert self.doors[direction] == None
        room = Room(program)
        try:
            room = rooms[room.name]
        except KeyError:
            pass
        self.doors[direction] = room
        return room

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        if other is None:
            return False
        return self.name < other.name

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __repr__(self):
        doors = ", ".join(
            f"{direction}: {room.name if room else None}" for direction, room in self.doors.items()
        )
        return f"{self.name}: {doors=}"


def get_path(start, end):
    if start is None or end is None or "Pressure-Sensitive" in start.name:
        return []

    frontier = []
    heapq.heappush(frontier, (0, start))

    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        s, room = heapq.heappop(frontier)
        if room == end:
            break

        for direction, next_room in room.doors.items():
            new_cost = cost_so_far[room] + 1
            if next_room is None:
                continue
            if next_room and (next_room not in cost_so_far or new_cost < cost_so_far[next_room]):
                cost_so_far[next_room] = new_cost
                priority = new_cost
                heapq.heappush(frontier, (priority, next_room))
                came_from[next_room] = (room, direction)

    out = []
    room = end
    while room != start:
        room, direction = came_from[room]
        out.insert(0, direction)
    return out


class Game:
    def __init__(self, instructions, rooms):
        self.cpu = intcode.IntCode(instructions, [])
        self.process("")
        self.room = Room(self.cpu)
        self.rooms = rooms
        self.inventory = []
        self.backup = self.cpu.clone()

        # Now let's build the room graph
        self.paths = {
            (start_room, end_room): get_path(start_room, end_room)
            for start_room in rooms.values()
            for end_room in rooms.values()
        }

    def save(self):
        self.backup_inventory = self.inventory[::]
        self.backup_room = self.room
        self.backup = self.cpu.clone()

    def load(self):
        self.inventory = self.backup_inventory[::]
        self.room = self.backup_room
        self.cpu = self.backup.clone()

    def process(self, input):
        self.cpu.inputs = [ord(c) for c in (input + "\n")]
        self.cpu.output = []
        while True:
            try:
                self.cpu.resume()

            except (intcode.Halted, intcode.InputStall):
                pass
            if not self.cpu.output:
                continue
            break
        return self.cpu.output

    def move(self, direction):
        self.process(direction)
        self.room = Room(self.cpu)
        return self.rooms[self.room.name]

    def drop(self, item):
        output = self.process(f"drop {item}")
        self.inventory.remove(item)
        return "".join(chr(c) for c in output)

    def move_to_room(self, target):
        path = self.paths[self.room, target]
        for step in path:
            game.move(step)

    def take(self, item):
        output = self.process(f"take {item}")
        self.inventory.append(item)
        return "".join(chr(c) for c in output)


with open(sys.argv[1], "r") as file:
    instructions = []
    for line in file:
        instructions.extend([int(v) for v in line.strip().split(",")])

program = intcode.IntCode(instructions, [])

rooms = {}

while True:
    try:
        program.resume()

    except (intcode.Halted, intcode.InputStall):
        pass
    if not program.output:
        continue
    break
room = Room(program)
rooms[room.name] = room

frontier = [(room, door) for door in room.doors]

while frontier:
    room, door = frontier.pop(0)

    new_room = room.take(door, rooms)
    print(f"{room} -> {new_room}")
    if new_room.name in rooms:
        continue

    rooms[new_room.name] = new_room
    frontier.extend([(new_room, door) for door in new_room.doors])

for room in rooms.values():
    print(room)
    print(room.description, room.items)
    print("---")


# Now we know our way around, we'll spin up a fresh machine and collect all the items, paying no attention to
# the shortest path because who cares
game = Game(instructions, rooms)

bad_items = {"escape pod", "photons", "infinite loop", "molten lava", "giant electromagnet"}

item_rooms = [room for room in rooms.values() if room.items]

for item_room in item_rooms:
    game.move_to_room(item_room)

    for item in item_room.items:
        if item in bad_items:
            continue
        print("Taking", item)
        print(game.take(item))

game.move_to_room(rooms["Security Checkpoint"])

game.save()

for item_set in powerset(game.inventory):
    game.load()

    for item in item_set:
        game.drop(item)
    game.move_to_room(rooms["Pressure-Sensitive Floor"])
    if game.room.code:
        print(game.room.code)
        break
