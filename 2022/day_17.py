import sys

with open(sys.argv[1], 'r') as file:
    winds = file.read().strip()


def bit_width(n):
    width = 0
    while n:
        width += 1
        n >>= 1
    return width

grid_width = 7

class Shape:
    def __init__(self, num):
        self.rows = []
        self.num = num
        self.width = 0

        while num:
            self.rows.append(num & 0x7f)
            num >>= 7

        self.width = max((bit_width(row) for row in self.rows))
        self.height = len(self.rows)
        self.current = num
        self.current_pos = (0,0)

    def set_pos(self, x, y):
        num = self.num << ((7-x) - self.width)
        num <<= (7*y)
        self.current_pos = (x, y)
        self.current = num
        #print(self.current)

    def move(self, cavern, x, y):
        # Hitting a wall with a left or right movement means a bit has changed row. I think this will just be 1 or -1 for now
        #print('move',x,y,self.current_pos,self.current)
        new = self.current
        if x == 1:
            new >>= 1
            if any( (self.current & (1 << (n*7)) for n in range(self.highest())) ):
                return False
        elif x == -1:
            new <<= 1
            if any( (self.current & (1 << (n*7+6)) for n in range(self.highest())) ):
                return False

        # Dropping it down certainly won't work if we've got anything on the bottom row
        if y == -1:
            new >>= 7
            if self.current & 0x7f or self.current_pos[1] == 0:
                return False

        can_move = 0 == (new & cavern.grid)

        if can_move:
            self.current = new
            self.current_pos = (self.current_pos[0] + x, self.current_pos[1] + y)

        return can_move

    def highest(self):
        return self.current_pos[1] + self.height

    def __repr__(self):
        num = self.current
        out = ['+------+']

        while num:
            out.append('|' + ''.join(('#' if (num & (1<<(6-n))) else '.' for n in range(7))) + '|')
            num >>= 7

        out.reverse()
        return '\n'.join(out)



shapes = [0b1111, #line
          0b000001000001110000010, #cross
          0b000000100000010000111, #back-l
          0b0000001000000100000010000001, #vert
          0b00000110000011]

shapes = [Shape(shape) for shape in shapes]


class Cavern:
    def __init__(self):
        self.grid = 0
        self.last = 0
        self.highest = 0

    def __repr__(self):
        num = self.grid
        out = ['+------+']

        while num:
            out.append('|' + ''.join(('#' if (num & (1<<(6-n))) else '.' for n in range(7))) + '|')
            num >>= 7

        out.reverse()
        return '\n'.join(out)

    def fix(self, obj):
        self.grid |= obj.current
        self.highest = max(self.highest, obj.highest())

    def top_rows(self, n):
        return self.grid >> max(0, ((self.highest - n)*7))

def get_height(target):
    wind_movement = {'<': -1, '>' : 1}

    obj_index = 0
    wind_index = 0
    cavern = Cavern()

    states = {}

    step = 0
    extra = 0
    while step < target:
        can_move = True

        while can_move:
            state = obj_index, wind_index, cavern.top_rows(20)

            if state in states:
                old_step, old_highest = states[state]
                higher = cavern.highest - old_highest

                jump_steps = step - old_step
                #Every old_steps we increase highest by higher, so we can skip some multiples of that
                todo = target - step
                jumps = todo // jump_steps
                step += jumps * jump_steps

                extra += higher * jumps
            else:
                states[state] = (step, cavern.highest)
            obj = shapes[obj_index]
            obj_index = (obj_index + 1) % len(shapes)

            obj.set_pos(2, cavern.highest + 3)

            while can_move:
                wind = winds[wind_index]
                wind_index = (wind_index + 1) % len(winds)

                # Do the wind movement
                obj.move(cavern, wind_movement[wind], 0)
                can_move = obj.move(cavern, 0, -1)


        # Now we set the object into the cavern
        cavern.fix(obj)
        step += 1

    return cavern.highest + extra

print(get_height(2022))
print(get_height(10**12))
