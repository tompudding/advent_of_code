import sys
import re


class RulePart:
    def __init__(self, text):
        if text == "A":
            self.func = lambda x: True
            self.result = "A"
            return
        elif text == "R":
            self.func = lambda x: True
            self.result = "R"
            return

        try:
            rule, self.result = text.split(":")
        except ValueError:
            self.result = text
            self.func = lambda x: True
            return

        if "<" in rule:
            func = self.less_than
            splitter = "<"
        elif ">" in rule:
            func = self.greater_than
            splitter = ">"
        else:
            print("bad rule", rule)
            raise jim

        operand, constant = rule.split(splitter)
        self.operand = "xmas".index(operand)
        self.constant = int(constant)

        self.func = func

    def less_than(self, workflow):
        return workflow.parts[self.operand] < self.constant

    def greater_than(self, workflow):
        return workflow.parts[self.operand] > self.constant


class Rule:
    def __init__(self, text):
        self.name, rest = text.split("{")
        parts = rest.strip("}").split(",")
        self.parts = [RulePart(part) for part in parts]

    def operate(self, workflow):
        for rule in self.parts:
            if rule.func(workflow):
                return rule.result

        return "R"


class Workflow:
    def __init__(self, text):
        self.parts = [
            int(part) for part in re.match("{x=([\d]+),m=([\d]+),a=([\d]+),s=([\d]+)}", text).groups()
        ]

    def total(self):
        return sum(self.parts)

    def __repr__(self):
        return f"{{x={self.parts[0]},m={self.parts[1]},a={self.parts[2]},s={self.parts[3]}}}"


with open(sys.argv[1], "r") as file:
    lines = [line.strip() for line in file]

gap = lines.index("")
rules, workflows = lines[:gap], lines[gap + 1 :]
rules, workflows = [Rule(rule) for rule in rules], [Workflow(workflow) for workflow in workflows]

rules = {rule.name: rule for rule in rules}

accepted = []

for workflow in workflows:
    rule_name = "in"

    while True:
        rule_name = rules[rule_name].operate(workflow)

        if rule_name == "A":
            accepted.append(workflow)
            break
        elif rule_name == "R":
            break

print(accepted)
print(sum(workflow.total() for workflow in accepted))
