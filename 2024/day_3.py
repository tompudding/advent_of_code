import re
import sys

with open(sys.argv[1],'r') as file:
    data = file.read()

mul_expr = r'mul\((\d\d?\d?),(\d\d?\d?)\)'

print(sum((int(x)*int(y)) for x,y in re.findall(r'mul\((\d\d?\d?),(\d\d?\d?)\)', data)))

enabled = True
total = 0
for match in re.finditer(rf"(do\(\)|don't\(\)|{mul_expr})",data):
    matched = match.group(1)

    match matched:
        case 'do()':
            enabled = True
        case "don't()":
            enabled = False
        case matched if matched.startswith('mul') and enabled:
            x, y = match.groups()[1:]
            total += int(x)*int(y)

print(total)
