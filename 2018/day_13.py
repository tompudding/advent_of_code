import sys
from collections import defaultdict
from colorama import Fore, Back, Style


class Directions:
    LEFT = complex(-1, 0)
    RIGHT = complex(1, 0)
    UP = complex(0, -1)
    DOWN = complex(0, 1)

    ALL = [LEFT, RIGHT, UP, DOWN]

    opposite = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}
    from_cart = {"v": DOWN, "^": UP, "<": LEFT, ">": RIGHT}
    to_cart = {v: k for k, v in from_cart.items()}


class Rotations:
    LEFT = complex(0, -1)
    STRAIGHT = complex(1, 0)
    RIGHT = complex(0, 1)


class Cart:
    turns = [Rotations.LEFT, Rotations.STRAIGHT, Rotations.RIGHT]

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction
        self.next_turn = 0
        self.remove = False

    def step(self, system):
        x = system.adjacency[self.pos, self.direction]
        try:
            new_pos, new_dir = system.adjacency[self.pos, self.direction]
        except:
            print(self.pos, self.direction, system.adjacency[self.pos, self.direction])
            raise
        self.pos = new_pos
        self.direction = new_dir
        if self.pos in system.intersections:
            turn = self.turns[self.next_turn]
            self.next_turn = (self.next_turn + 1) % len(self.turns)
            self.direction *= turn

    def __repr__(self):
        return Fore.WHITE + Style.BRIGHT + Directions.to_cart[self.direction] + Style.RESET_ALL + Fore.RESET


class CartSystem:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = max(len(line) for line in lines)

        self.adjacency = {}
        self.grid = {}
        self.carts = []
        self.intersections = set()

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                pos = complex(x, y)

                if not char.strip():
                    continue
                self.grid[pos] = char
                match char:
                    case "-":
                        direction = target_dir = Directions.RIGHT
                    case "|":
                        direction = target_dir = Directions.UP
                    case "/":
                        # We need to decide if this is a top-left corner or a bottom right corner. It's bottom
                        # right if immediately left of it (which we've already processed) is a '-'
                        try:
                            is_bottom_right = self.grid[pos + Directions.LEFT] in "-+"
                        except KeyError:
                            is_bottom_right = False
                        if is_bottom_right:
                            direction, target_dir = Directions.RIGHT, Directions.UP
                        else:
                            direction, target_dir = Directions.LEFT, Directions.DOWN
                    case "\\":
                        try:
                            is_top_right = self.grid[pos + Directions.LEFT] in "-+"
                        except KeyError:
                            is_top_right = False
                        if is_top_right:
                            direction, target_dir = Directions.RIGHT, Directions.DOWN
                        else:
                            direction, target_dir = Directions.LEFT, Directions.UP
                    case ">" | "<" | "v" | "^":
                        self.carts.append(Cart(pos, Directions.from_cart[char]))
                        if char in "<>":
                            self.grid[pos] = "-"
                            direction = target_dir = Directions.RIGHT
                        else:
                            self.grid[pos] = "|"
                            direction = target_dir = Directions.UP
                    case "+":
                        self.intersections.add(pos)
                        self.grid[pos] = char
                        continue
                    case _:
                        raise InputError()
                        continue

                assert (pos, direction) not in self.adjacency
                self.adjacency[pos, direction] = (pos + target_dir, target_dir)
                # flip it
                direction, target_dir = Directions.opposite[target_dir], Directions.opposite[direction]
                assert (pos, direction) not in self.adjacency
                self.adjacency[pos, direction] = (pos + target_dir, target_dir)

        for pos in self.intersections:
            for direction in Directions.ALL:
                self.adjacency[pos, direction] = (pos + direction, direction)

        self.carts.sort(key=lambda x: (x.pos.real, x.pos.imag))
        self.cart_positions = {cart.pos: cart for cart in self.carts}

    def step(self, first_crash=False):
        collision = False
        carts = list(self.carts)
        for cart in carts:
            if cart.remove:
                continue
            del self.cart_positions[cart.pos]
            cart.step(self)
            if cart.pos in self.cart_positions and not self.cart_positions[cart.pos].remove:
                if first_crash:
                    return cart.pos
                else:
                    # Remove both carts
                    cart.remove = self.cart_positions[cart.pos].remove = True

            self.cart_positions[cart.pos] = cart
        self.carts = sorted(
            [cart for cart in carts if not cart.remove], key=lambda x: (x.pos.real, x.pos.imag)
        )

        return None

    def __repr__(self):
        out = []
        carts = {cart.pos: cart for cart in self.carts}
        for y in range(self.height):
            row = []
            for x in range(self.width):
                pos = complex(x, y)
                try:
                    char = repr(carts[pos])
                except KeyError:
                    try:
                        char = self.grid[pos]
                    except KeyError:
                        char = " "
                row.append(char)
            out.append("".join(row))
        return "\n".join(out)


with open(sys.argv[1]) as file:
    cart_system = CartSystem(file.readlines())

for i in range(2000):
    pos = cart_system.step(first_crash=True)
    if pos:
        print(",".join((str(int(part)) for part in (pos.real, pos.imag))))
        break

    # input()
with open(sys.argv[1]) as file:
    cart_system = CartSystem(file.readlines())

while True:
    cart_system.step(first_crash=False)
    if len(cart_system.carts) == 1:
        pos = cart_system.carts[0].pos
        print(",".join((str(int(part)) for part in (pos.real, pos.imag))))
        break
