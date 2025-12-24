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


def cook(recipes, elves, num_recipes):
    next = sum(recipes[elf] for elf in elves)
    if next >= 10:
        recipes[num_recipes] = 1
        num_recipes += 1
    recipes[num_recipes] = next % 10
    num_recipes += 1

    elves[0] = (recipes[elves[0]] + 1 + elves[0]) % num_recipes
    elves[1] = (recipes[elves[1]] + 1 + elves[1]) % num_recipes

    return num_recipes


with open(sys.argv[1]) as file:
    num = int(file.read().strip())

recipes = bytearray(21000000)
recipes[:2] = [3, 7]
num_recipes = 2
elves = [0, 1]

while num_recipes < num + 10:
    num_recipes = cook(recipes, elves, num_recipes)

print("".join(f"{d}" for d in recipes[num : num + 10]))

matched_pos = matched = 0
target_digits = bytearray(full_digits(num, 6))


while True:
    num_recipes = cook(recipes, elves, num_recipes)

    while matched_pos < num_recipes - len(target_digits):
        if recipes[matched_pos] == target_digits[matched]:
            matched += 1
            if matched == len(target_digits):
                print(matched_pos + 1 - matched)
                raise SystemExit()
        else:
            matched = 0
        matched_pos += 1
