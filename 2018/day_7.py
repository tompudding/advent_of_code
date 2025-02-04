import sys
from collections import defaultdict


def time_for(step):
    return


class WorkerPool:
    def __init__(self, num_workers, fixed_time):
        self.workers = [(0, None) for i in range(num_workers)]
        self.fixed = fixed_time
        self.todo = []

    def time_for(self, step):
        if not step:
            return 0
        return self.fixed + ord(step) - ord("A") + 1

    def complete(self, time):
        out = []
        for i in range(len(self.workers)):
            finish, step = self.workers[i]
            if step is None:
                continue
            if time >= finish:
                out.append(step)
                next = self.todo.pop(0) if self.todo else None
                self.workers[i] = (time + self.time_for(next), next)
        return out

    def perform(self, step, time):
        for i in range(len(self.workers)):
            finish, working_on = self.workers[i]

            if working_on is None:
                self.workers[i] = (time + self.time_for(step), step)
                return
        self.todo.append(step)

    def available(self):
        return any(working_on is None for finish, working_on in self.workers)

    def __contains__(self, step):
        return any(working_on == step for finish, working_on in self.workers)


required = defaultdict(set)
all_steps = set()

with open(sys.argv[1], "r") as file:
    for line in file:
        parts = line.split()
        needed, target = parts[1], parts[7]
        required[target].add(needed)
        all_steps |= {target, needed}


done = []
open = sorted([step for step in all_steps if not required[step]])

while open:
    done.append(open.pop(0))

    if done == all_steps:
        break

    open = sorted(
        [
            step
            for step in all_steps
            if (step not in done) and (not required[step] or all(x in done for x in required[step]))
        ]
    )
    print(open, done)

print("".join(done))

example = len(required) < 10
pool = WorkerPool(num_workers=2 if example else 5, fixed_time=0 if example else 60)

done = []


def processing(step):
    return step in done or step in pool


open = sorted([step for step in all_steps if not required[step]])
time = 0

while len(done) != len(all_steps):
    completed = pool.complete(time)
    done.extend(completed)
    open = sorted(
        [
            step
            for step in all_steps
            if (not processing(step)) and (not required[step] or all(x in done for x in required[step]))
        ]
    )
    while open and pool.available():
        step = open.pop(0)
        pool.perform(step, time)

    if len(done) == len(all_steps):
        break
    time += 1

    if not completed:
        continue

print(time)
