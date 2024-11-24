import sys

lookups = {}


class Recipe:
    num = 0

    def __init__(self, parts, result):
        self.parts = parts
        self.result = result
        self.ore_required = None


class Amount:
    def __init__(self, name, num):
        self.num = num
        self.name = name


def parse_amount(input):
    num, name = input.split()
    return Amount(name, int(num))


def produce_fuel(recipe, surplus, fuel_required):
    ore = 0
    required = {part.name: part.num * fuel_required for part in fuel_recipe.parts}

    while required:
        name = next(iter(required))

        num = required.pop(name)

        # Firstly we check if this can be serviced by the surplus

        if name in surplus:
            if surplus[name] >= num:
                # No problem
                surplus[name] -= num
                continue

            # Otherwise we just reduce the amount we need
            num -= surplus[name]
            surplus[name] = 0

        target_recipe = lookups[name]

        # How many copies of this recipe will we need? We divide our requirement by the provided, rounded up

        copies = (num + target_recipe.result.num - 1) // target_recipe.result.num

        produced = copies * target_recipe.result.num
        if produced > num:
            try:
                surplus[name] += produced - num
            except KeyError:
                surplus[name] = produced - num

        # Add that many copies of the product. Keep track of ore separately
        for part in target_recipe.parts:
            consume = copies * part.num
            # print(f"Consume {consume} {part.name} to produce {produced} {name}")

            if part.name == "ORE":
                ore += consume
            else:
                try:
                    required[part.name] += consume
                except KeyError:
                    required[part.name] = consume
    return ore, surplus


with open(sys.argv[1], "r") as file:
    for line in file:
        parts, result = line.strip().split(" => ")
        parts = [parse_amount(c.strip()) for c in parts.split(",")]

        recipe = Recipe(parts, parse_amount(result))

        lookups[recipe.result.name] = recipe

fuel_recipe = lookups["FUEL"]
assert fuel_recipe.result.num == 1

surplus = {}
ore_for_one_fuel, surplus = produce_fuel(fuel_recipe, surplus, 1)
original_surplus = {name: num for name, num in surplus.items()}

print(ore_for_one_fuel)

ore_available = 1000000000000

min_fuel = ore_available // ore_for_one_fuel
# TODO: work out the max sensibly?
max_fuel = min_fuel + 10000000

while min_fuel < max_fuel - 1:
    mid = min_fuel + (max_fuel - min_fuel) // 2

    print("Test", mid, min_fuel, max_fuel)
    ore, surplus = produce_fuel(fuel_recipe, {}, mid)

    if ore > ore_available:
        # We can't do that one
        max_fuel = mid
    elif ore < ore_available:
        min_fuel = mid

print(min_fuel)
