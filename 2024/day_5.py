import sys
import functools


class Rule:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"{self.a} < {self.b}"


class Update:
    def __init__(self, numbers):
        self.numbers = numbers
        self.positions = {num: i for i, num in enumerate(self.numbers)}

    def is_valid(self, rules):
        for rule in rules:
            try:
                if self.positions[rule.a] >= self.positions[rule.b]:
                    return False
            except KeyError:
                continue

        return True

    def middle(self):
        assert len(self.numbers) & 1
        return self.numbers[len(self.numbers) // 2]

    def sort(self, compare):
        self.numbers.sort(key=functools.cmp_to_key(compare))


rules = []
updates = []

parsing_rules = True
with open(sys.argv[1], "r") as file:
    for line in file:
        line = line.strip()
        if parsing_rules:
            try:
                rules.append(Rule(*(int(v) for v in line.split("|"))))
            except ValueError:
                parsing_rules = False
        else:
            updates.append(Update([int(v) for v in line.split(",")]))

rules_by_num = {}

for rule in rules:
    try:
        rules_by_num[rule.a].add(rule.b)
    except KeyError:
        rules_by_num[rule.a] = {rule.b}


def compare(a, b):
    try:
        if b in rules_by_num[a]:
            return -1
    except KeyError:
        pass

    try:
        if a in rules_by_num[b]:
            return 1
    except KeyError:
        pass
    return 0


valid = []
not_valid = []
for update in updates:
    (valid if update.is_valid(rules) else not_valid).append(update)

print(sum(update.middle() for update in valid))

for update in not_valid:
    update.sort(compare)

print(sum(update.middle() for update in not_valid))
