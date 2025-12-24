import sys


def digits(num):
    if num >= 10:
        yield 1
    yield num % 10


def full_digits(num, length):
    out = []
    for i in range(length):
        out.append(num % 10)
        num //= 10
    return list(reversed(out))


with open(sys.argv[1]) as file:
    num = int(file.read().strip())

recipes = [3, 7]
elves = [0, 1]

while len(recipes) < num + 10:
    new_recipes = digits(sum(recipes[elf] for elf in elves))
    recipes.extend(new_recipes)
    elves = [(elf + 1 + recipes[elf]) % len(recipes) for elf in elves]

print("".join(f"{d}" for d in recipes[num : num + 10]))

recipes = [3, 7]
elves = [0, 1]
matched_pos = 0
target_digits = full_digits(num, 6)

while True:
    new_recipes = digits(sum(recipes[elf] for elf in elves))
    recipes.extend(new_recipes)
    elves = [(elf + 1 + recipes[elf]) % len(recipes) for elf in elves]

    while matched_pos < len(recipes) - len(target_digits):
        if recipes[matched_pos : matched_pos + len(target_digits)] == target_digits:
            print(matched_pos)
            raise SystemExit()
        matched_pos += 1
