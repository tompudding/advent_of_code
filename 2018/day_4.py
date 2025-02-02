import sys
from datetime import datetime
from collections import Counter


class Guard:
    def __init__(self, id):
        self.id = id
        self.sleep_time = None
        self.sleeps = Counter()

    def sleep(self, stamp):
        self.sleep_time = stamp.minute

    def wake(self, stamp):
        self.sleeps.update(range(self.sleep_time, stamp.minute))


data = []
with open(sys.argv[1], "r") as file:
    for line in file:
        date, rest = line.strip()[1:].split("] ", 1)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        data.append((date, rest))

data.sort()

guards = {}
guard = None

for date, info in data:
    if "Guard" in info:
        id = int(info.split("#")[1].split()[0])
        try:
            guard = guards[id]
        except KeyError:
            guard = Guard(id)
            guards[id] = guard

    elif "asleep" in info:
        guard.sleep(date)
    elif "wakes" in info:
        guard.wake(date)
    else:
        raise Jimbo

    # print(date, rest)
guards = sorted([guard for guard in guards.values()], key=lambda guard: -guard.sleeps.total())

sleepiest = guards[0]
print(sleepiest.sleeps.most_common(1)[0][0] * sleepiest.id)

minutes = sorted(
    [(guard.id, guard.sleeps.most_common(1)[0]) for guard in guards if guard.sleeps], key=lambda x: -x[1][1]
)
print(minutes[0][0] * minutes[0][1][0])
