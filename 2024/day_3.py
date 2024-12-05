import re
import sys

with open(sys.argv[1], "r") as file:
    data = file.read()

mul_expr = rf"mul\((\d{{1,3}}),(\d{{1,3}})\)"

print(sum((int(x) * int(y)) for x, y in re.findall(mul_expr, data)))

enabled = True
total = 0
for match in re.finditer(rf"(do\(\)|don't\(\)|{mul_expr})", data):
    match match.groups():
        case ("do()", *_):
            enabled = True
        case ("don't()", *_):
            enabled = False
        case (mul, x, y) if mul.startswith("mul") and enabled:
            total += int(x) * int(y)

print(total)
