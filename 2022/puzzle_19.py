import sys
import re
import functools


# @functools.total_ordering
class Resources:
    def __init__(self, ore=0, clay=0, obsidian=0, geodes=0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geodes = geodes
        self.resources = (self.ore, self.clay, self.obsidian, self.geodes)

    def __add__(self, other):
        return Resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geodes + other.geodes,
        )

    def copy(self):
        return Resources(*self.resources)

    # def __hash__(self):
    #     return hash(self.resources)

    # def __eq__(self, other):
    #     return self.resources == other.resources

    # def __lt__(self, other):
    #     return self.resources < other.resources

    def __repr__(self):
        return f"ore={self.ore} clay={self.clay} obsidian={self.obsidian} geodes={self.geodes}"


# @functools.total_ordering
class Robots:
    def __init__(self, ore=0, clay=0, obsidian=0, geode=0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode
        self.robots = (self.ore, self.clay, self.obsidian, self.geode)

    def generate(self):
        return Resources(self.ore, self.clay, self.obsidian, self.geode)

    def __add__(self, other):
        return Robots(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    # def __hash__(self):
    #     return hash(self.robots)

    # def __eq__(self, other):
    #     return self.robots == other.robots

    # def __lt__(self, other):
    #     return self.robots < other.robots

    def copy(self):
        return Robots(*self.robots)

    def __repr__(self):
        return f"ore_robots={self.ore} clay_robots={self.clay} obsidian_robots={self.obsidian} geodes_robots={self.geode}"


class Recipe:
    def __init__(self, ore, clay=0, obsidian=0, builds=None):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.builds = builds

        self.required = [self.ore, self.clay, self.obsidian, 0]

    def can_build(self, resources, robots):
        return (
            resources.ore >= self.ore and resources.clay >= self.clay and resources.obsidian >= self.obsidian
        )

    def build(self, resources, robots):
        # Check if we have enough. Note that geodes aren't ever used in recipes
        if resources.ore < self.ore or resources.clay < self.clay or resources.obsidian < self.obsidian:
            return None, None

        # We can build it!
        new_resources = Resources(
            resources.ore - self.ore,
            resources.clay - self.clay,
            resources.obsidian - self.obsidian,
            resources.geodes,
        )
        new_robots = robots + self.builds

        return new_resources, new_robots

    def __repr__(self):
        out = [f"{self.ore} ore"]
        if self.clay:
            out.append(f", {self.clay} clay")
        if self.obsidian:
            out.append(f", {self.obsidian} obsidian")
        out.append(".")
        return "".join(out)


class Blueprint:
    def __init__(self, ore_robot, clay_robot, obsidian_robot, geode_robot):
        self.ore_robot = ore_robot
        self.clay_robot = clay_robot
        self.obsidian_robot = obsidian_robot
        self.geode_robot = geode_robot
        self.recipes = [self.ore_robot, self.clay_robot, self.obsidian_robot, self.geode_robot]
        self.most_demanding = []

        for choice in range(4):
            self.most_demanding.append(
                max(
                    robot.required[choice]
                    for robot in (self.ore_robot, self.clay_robot, self.obsidian_robot, self.geode_robot)
                )
            )

    def __repr__(self):
        return f"Ore: {self.ore_robot} Clay: {self.clay_robot} Obsidian: {self.obsidian_robot} Geode: {self.geode_robot}"


class State:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.amounts = Resources()
        self.robots = Robots(ore=1)
        self.cache = {}
        self.best = 0

        print(self.blueprint.most_demanding)

    def simulate(self, time, resources, robots):
        # We see what we could win if we built everything we could build at every step. It's an upper bound
        # that will help us prune hopeless branches

        for t in range(time):
            # The current robots generate extra stuff

            resources += robots.generate()

            if self.blueprint.recipes[0].can_build(resources, robots):
                robots.ore += 1
            if self.blueprint.recipes[1].can_build(resources, robots):
                robots.clay += 1
            if self.blueprint.recipes[2].can_build(resources, robots):
                robots.obsidian += 1

            if self.blueprint.recipes[3].can_build(resources, robots):
                resources, robots = self.blueprint.recipes[3].build(resources, robots)

        return resources.geodes

    def best_geodes(self, time, resources, robots, choices):

        if time == 0:
            # we're done
            return resources.geodes, choices

        # print(time, self.best, resources, robots)
        # print(choices)

        # A very basic prune is to stop if we don't have enough time to make enough geodes so that we'll be the best
        # Assume that we can generate 1 obsidian robot per round

        max_geodes = self.simulate(time, resources.copy(), robots.copy())

        if max_geodes < self.best or max_geodes == 0:
            return resources.geodes, choices

        if max_geodes < self.best:
            return resources.geodes, choices

        if max_geodes == 0:
            return resources.geodes, choices

        # if (time, resources, robots) in self.cache:
        #    return self.cache[(time, resources, robots)]

        generated_resources = robots.generate()

        best_geodes = 0
        best_choices = None
        num_geodes = 0

        # Firstly if we can build a geode we should

        options = [3, 2, 1, 0, None]

        # I got this from reddit and I don't understand it at all
        if self.blueprint.recipes[2].can_build(resources, robots):
            options = [3, 2, None]

        for choice in options:

            # We don't need to build a robot of this type if we're producing enough already, which is enough
            # each round to make the most demanding robot
            if choice is None:
                num_geodes, new_choices = self.best_geodes(
                    time - 1, resources + generated_resources, robots, choices + [None]
                )
            else:

                if choice != 3 and robots.robots[choice] >= self.blueprint.most_demanding[choice]:
                    continue

                new_choices = choices + [choice]
                new_resources, new_robots = self.blueprint.recipes[choice].build(resources, robots)
                if new_robots:
                    num_geodes, new_choices = self.best_geodes(
                        time - 1, new_resources + generated_resources, new_robots, new_choices
                    )

            if num_geodes > best_geodes:
                best_geodes = num_geodes
                best_choices = new_choices

            if best_geodes > self.best:
                self.best = best_geodes

            if choice == 3 and new_robots:
                # print("beak", best_geodes)
                break

        # if best_choices:
        #    self.cache[time, resources, robots] = best_geodes, best_choices[-time:]

        return best_geodes, best_choices


blueprints = []

with open(sys.argv[1], "r") as file:
    for line in file:
        match = re.match(
            "Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
            line.strip(),
        )
        data = [int(item) for item in match.groups()]
        if not match:
            continue
        ore = Recipe(data[1], builds=Robots(ore=1))
        clay = Recipe(data[2], builds=Robots(clay=1))
        obsidian = Recipe(*data[3:5], builds=Robots(obsidian=1))
        geode = Recipe(data[5], 0, data[6], builds=Robots(geode=1))

        blueprints.append(Blueprint(ore, clay, obsidian, geode))

quality = 0
for i, blueprint in enumerate(blueprints):
    print(f"Blueprint {i+1}: {blueprint}")
    state = State(blueprint)

    geodes, choices = state.best_geodes(24, state.amounts, state.robots, [])

    print(geodes)
    print(choices)
    quality += (i + 1) * geodes
    # break

print(quality)

total = 1
for blueprint in blueprints[:3]:
    state = State(blueprint)

    geodes, choices = state.best_geodes(32, state.amounts, state.robots, [])
    total *= geodes
    print(geodes)

print(total)
# Let's be super basic and recuse all possibilities. I'm sure part 2 is to do a billion years or something.
