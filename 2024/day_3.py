import re
import sys

with open(sys.argv[1],'r') as file:
    data = file.read()

mul_expr = r'mul\((\d\d?\d?),(\d\d?\d?)\)'

print(sum((int(x)*int(y)) for x,y in re.findall(r'mul\((\d\d?\d?),(\d\d?\d?)\)', data)))

enabled = True
total = 0
for match in re.finditer(rf"(do\(\)|don't\(\)|{mul_expr})",data):
    match match.groups():
        case ('do()', *_):
            enabled = True
        case ("don't()", *_):
            enabled = False
        case (mul, x, y) if mul.startswith('mul') and enabled:
            total += int(x)*int(y)

print(total)
