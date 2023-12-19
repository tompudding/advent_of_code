import sys
import re


class RulePart:
    def __init__(self, text):
        self.text = text
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

    def apply_range(self, workflow_range):
        # We want to create two new ranges, one for if our criteria matches, and one for when it doesn't. If
        # either is empty we return None
        if self.func == self.less_than:
            return workflow_range.constrain(self.operand, maximum=self.constant), workflow_range.constrain(
                self.operand, minimum=self.constant
            )

        if self.func == self.greater_than:
            return workflow_range.constrain(
                self.operand, minimum=self.constant + 1
            ), workflow_range.constrain(self.operand, maximum=self.constant + 1)

        if self.result == "R":
            return None, workflow_range

        return workflow_range, None

    def __repr__(self):
        return self.text


class WorkflowRange:
    def __init__(self, x_range=(1, 4001), m_range=(1, 4001), a_range=(1, 4001), s_range=(1, 4001)):
        self.ranges = [list(x_range), list(m_range), list(a_range), list(s_range)]

    def constrain(self, operand, minimum=0, maximum=4001):
        current_range = self.ranges[operand]
        new_range = [max(minimum, current_range[0]), min(maximum, current_range[1])]
        new_ranges = list(self.ranges)
        new_ranges[operand] = new_range
        return WorkflowRange(*new_ranges)

    def __len__(self):
        product = 1

        for r in self.ranges:
            product *= r[1] - r[0]

        return product

    def __repr__(self):
        return f"{{x={self.ranges[0][0]}-{self.ranges[0][1]-1}, m={self.ranges[1][0]}-{self.ranges[1][1]-1}, a={self.ranges[2][0]}-{self.ranges[2][1]-1}, s={self.ranges[3][0]}-{self.ranges[3][1]-1}}}"


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

    def operate_range(self, rules, workflow_range):
        total = 0

        if len(workflow_range) == 0:
            return 0

        for rule in self.parts:
            if not workflow_range:
                break
            success_range, failure_range = rule.apply_range(workflow_range)

            if rule.result == "A":
                total += len(success_range)

            elif rule.result != "R":
                total += rules[rule.result].operate_range(rules, success_range)
            workflow_range = failure_range

        return total


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

print(sum(workflow.total() for workflow in accepted))

workflow_range = WorkflowRange()

print(rules["in"].operate_range(rules, workflow_range))
