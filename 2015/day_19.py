import sys
from dataclasses import dataclass
from collections import defaultdict
import heapq
from difflib import SequenceMatcher


@dataclass
class Replacement:
    orig: str
    new: str

    def backwards(self):
        return Replacement(new, orig)


with open(sys.argv[1], "r") as file:
    replacements_lines, molecule = file.read().split("\n\n")
    replacements = defaultdict(list)
    rev_replacements = defaultdict(list)
    for line in replacements_lines.splitlines():
        orig, new = line.split(" => ")
        replacement = Replacement(orig, new)

        replacements[replacement.orig].append(replacement)
        rev_replacements[replacement.new].append(replacement.backwards())

    molecule = molecule.strip()


def all_replacements(molecule, replacements):

    for i in range(len(molecule)):
        for orig, replacement_list in replacements.items():
            if molecule[i:].startswith(orig):
                for replacement in replacement_list:
                    yield molecule[:i] + replacement.new + molecule[i + len(orig) :], 1


def heuristic(state):
    return len(state)


print(len(set(all_replacements(molecule, replacements))))

# Part 2 wtf? Is it pathfinding?
frontier = []
start = molecule
heapq.heappush(frontier, (0, start))
cost_so_far = {start: 0}

while frontier:
    s, state = heapq.heappop(frontier)

    if state == "e":
        # Got it!
        break

    for next_state, cost in all_replacements(state, rev_replacements):
        new_cost = cost_so_far[state] + cost

        if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
            # came_from[next_state] = state
            cost_so_far[next_state] = new_cost
            priority = new_cost + heuristic(next_state)
            heapq.heappush(frontier, (priority, next_state))
else:
    print("Failed to find the path")
    raise Bad()

print(cost_so_far["e"])
