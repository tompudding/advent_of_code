import sys

class ALU:
    reg_names = 'wxyz'
    def __init__(self, input, instructions, verbose=False):
        self.regs = [0 for i in self.reg_names]
        self.input = [c for c in input]
        self.instructions = instructions
        self.pos = 0
        self.verbose = verbose

    def step(self, num):
        for mnemonic, operands in self.instructions[self.pos:self.pos+num]:
            values = alu.get_values(operands)
            functions[mnemonic](alu, operands, values)
            if self.verbose:
                print(f'Instruction {mnemonic} {operands} {alu}')
                if mnemonic == 'eql' and  operands[1] == 'w':
                    print('Equal' if self.regs[1] == 1 else 'BOO')
                

        self.pos += num

    def get_input(self):
        return int(self.input.pop(0))

    def set_reg(self, reg_name, val):
        self.regs[self.reg_names.index(reg_name)] = val

    def get_reg(self, reg_name):
        try:
            return self.regs[self.reg_names.index(reg_name)]
        except ValueError:
            return int(reg_name)

    def get_values(self, operands):
        return [self.get_reg(op) for op in operands]

    def __repr__(self):
        return f'w={self.regs[0]} x={self.regs[1]} y={self.regs[2]} z={self.regs[3]}'

def c_div(a, b):
    if a < 0:
        return -((-a)//b)
    return a//b

def inp(alu, operands, values):
    reg = operands[0]

    alu.set_reg(reg, alu.get_input())

def mul(alu, operands, values):
    alu.set_reg(operands[0], values[0]*values[1])

def add(alu, operands, values):
    alu.set_reg(operands[0], values[0]+values[1])

def div(alu, operands, values):
    alu.set_reg(operands[0], c_div(values[0], values[1]))

def mod(alu, operands, values):
    alu.set_reg(operands[0], values[0]%values[1])

def eql(alu, operands, values):
    alu.set_reg(operands[0], 1 if values[0] == values[1] else 0)
    

functions = {'inp' : inp, 'mul' : mul, 'add' : add, 'mod':mod, 'eql':eql, 'div':div}

with open(sys.argv[1], 'r') as file:
    lines = file.readlines()

instructions = []

for line in lines:
    line = line.strip()
    data = line.strip().split()

    instructions.append((data[0], data[1:]))

#Find the positions with a negative add to x, these are the ones that we can choose to keep z minimized. We might still be able to alter them actually and prevent it from getting too big, but let's try like this first
fixed = []
for i in range(0, len(instructions), 18):
    mnemonic, operands = instructions[i+5]
    print(mnemonic, operands)
    if int(operands[1]) < 0:
        fixed.append(i//18)
print(fixed)

#The first four characters can be anything I think
    
number = [1 for i in range(14)]

free_blocks = []
pos = 0
for i, fixed_num in enumerate(fixed):
    if fixed_num == pos:
        pos += 1
        continue
    print('a',fixed_num, pos)

    free_blocks.append( (pos, fixed_num-pos) )
    pos = fixed_num + 1

fixed_blocks = []

for i in range(len(free_blocks)):
    free_pos, free_len = free_blocks[i]
    fixed_start = free_pos + free_len
    try:
        fixed_end = free_blocks[i+1][0]
    except IndexError:
        fixed_end = 14
    fixed_len = fixed_end - fixed_start
    fixed_blocks.append((fixed_start, fixed_len))

print(free_blocks)
print(fixed_blocks)

free_positions = [0 for i in free_blocks]
current_block = 0

while current_block < len(free_positions):
    # Find a position for the current free block that works
    free_pos, free_len = free_blocks[current_block]
    fixed_pos, fixed_len = fixed_blocks[current_block]
    #print(f'{current_block=}')
    while free_positions[current_block] < 9**free_len:
        digits = free_positions[current_block]
        #print(f'{current_block=} {digits=}')
        for i in range(free_len):
            number[free_pos + free_len-1-i] = 1 + ((digits // (9**i)) % 9)

        free_positions[current_block] += 1
        if free_positions[current_block] >= 9**free_len:
            full = False
            free_positions[current_block] = 0
            break

        alu = ALU(number, instructions)
        #print('New ALU',number)

        #print(f'{free_pos=} {free_len=} {fixed_pos=} {fixed_len=}',number)

        num_stepped = 0
        full = True
        pos = 0

        # We need to step it up through the previous blocks too
        
        alu.step(18*(free_pos + free_len) + 6)

        #The fixed parts are fully determined by the last digit of the free part I think

        for i in range(fixed_len):
            x = alu.get_reg('x')
            if x >= 1 and x <= 9:
                number[fixed_pos+ i] = x
                alu.set_reg('w',x)
                alu.step(18)
                #print(f'{digits} is good', x, number)
                continue
            else:
                full = False
                break
            
        if not full:
            # we want to break out 
            continue
        else:
            #print('full',number)
            break
    if full:
        current_block += 1
    else:
        current_block -= 1

    if current_block < 0:
        print('yab')
        break
        

print(number)

alu = ALU(number, instructions, verbose=True)

alu.step(18*14)

    
            
print(''.join(f'{num}' for num in number))
    
# for pos in range(0,len(number)):
#     if pos in fixed:
#         #For this one we want to choose the number that will cancel with the negative
#         alu = ALU(number)
#         for mnemonic, operands in instructions[:18*pos+6]:
#             values = alu.get_values(operands)
#             functions[mnemonic](alu, operands, values)
            
#         x = alu.get_reg('x')
#         if x >= 1 and x <= 9:
#             number[pos] = x
#         else:
#             print('garf',x)
#             raise SystemExit()
#     min_z = 2**32
#     best = -1
#     for num in range(1,10):
#         number[pos] = num
#         alu = ALU(number)

#         for mnemonic, operands in instructions[:18*(pos+1)]:
#             values = alu.get_values(operands)
#             functions[mnemonic](alu, operands, values)
#             #print(f'Instruction {mnemonic} {operands} {alu}')

#         #print()
#         z = alu.get_reg('z')
#         if z < min_z:
#             min_z = z
#             best = num

#     print(pos, best)

# print(num, alu.get_reg('z'))
# print()


#digit[3] + 3 = digit[4]
#digit[3] + 11 + 2*digits[3]+6 + 9 
