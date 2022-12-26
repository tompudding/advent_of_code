import sys
import heapq


def heuristic(a, b):
    # Manhattan distance on a square grid
    return abs(a.pos[0] - b.pos[0]) + abs(a.pos[1] - b.pos[1])


class Breeze:
    def __init__(self, grid, pos):
        self.pos = pos
        self.grid = grid

    def get_pos(self, t):
        raise Bobbins


class NorthBreeze(Breeze):
    char = "^"

    def get_pos(self, t):
        return (self.pos[0], (self.pos[1] - t) % self.grid.height)


class SouthBreeze(Breeze):
    char = "v"

    def get_pos(self, t):
        return (self.pos[0], (self.pos[1] + t) % self.grid.height)


class EastBreeze(Breeze):
    char = ">"

    def get_pos(self, t):
        return (((self.pos[0] + t) % self.grid.width), self.pos[1])


class WestBreeze(Breeze):
    char = "<"

    def get_pos(self, t):
        return (((self.pos[0] - t) % self.grid.width), self.pos[1])


class WindyPops:
    wind_types = {wind.char: wind for wind in (NorthBreeze, SouthBreeze, EastBreeze, WestBreeze)}

    def __init__(self, lines):
        self.width = len(lines[1].strip()) - 2
        self.height = len(lines) - 2
        self.breezes = []
        for row, line in enumerate(lines[1:-1]):
            for col, char in enumerate(line[1:-1]):
                if char == ".":
                    continue
                self.breezes.append(self.wind_types[char](self, (col, row)))
        self.states = []
        self.start = (0, -1)
        self.end = (self.width - 1, self.height)
        self.walls = (
            {(x, -1) for x in range(-1, self.width + 1)}
            | {(self.width, y) for y in range(-1, self.height + 1)}
            | {(x, self.height) for x in range(-1, self.width + 1)}
            | {(-1, y) for y in range(-1, self.height + 1)}
        )
        self.walls.remove(self.start)
        self.walls.remove(self.end)
        state_map = set()
        t = 0
        while True:
            state = self.state_at_time(t)
            if state in state_map:
                # We have a cycle
                break
            t += 1
            state_map.add(state)
            self.states.append(set(state) | self.walls)

    def visualize(self, t):
        state = self.states[t % len(self.states)]
        out = []
        for row in range(self.height):
            line = []
            for col in range(self.width):
                if (col, row) in state:
                    line.append("x")
                else:
                    line.append(".")
            out.append("".join(line))
        return "\n".join(out)

    def state_at_time(self, t):
        grid = []
        for breeze in self.breezes:
            grid.append(breeze.get_pos(t))

        return tuple(grid)

    def neighbours(self, state):
        board_state = self.states[(state.t + 1) % len(self.states)]
        for diff in ((0, 1), (1, 0), (-1, 0), (0, -1), (0, 0)):
            new_pos = (state.pos[0] + diff[0], state.pos[1] + diff[1])
            if new_pos[0] < -1 or new_pos[1] < -1:
                continue
            if new_pos not in board_state:
                yield State(new_pos, state.t + 1)

    def get_path_length(self, start, end):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            s, current = heapq.heappop(frontier)

            if current.pos == end.pos:
                end = current
                break

            for next in self.neighbours(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(end, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        if current != end:
            raise ValueError("No path")
        return end


class State:
    def __init__(self, pos, t):
        self.pos = pos
        self.t = t
        self.all = (self.pos, self.t)

    def __hash__(self):
        return hash(self.all)

    def __lt__(self, other):
        return self.all < other.all

    def __eq__(self, other):
        return self.all == other.all


with open(sys.argv[1], "r") as file:
    windy_pops = WindyPops([line.strip() for line in file.readlines() if line.strip()])

end = State((windy_pops.width - 1, windy_pops.height), 0)
start = State((0, -1), 0)
end = windy_pops.get_path_length(start, end)
print(end.t)

back = windy_pops.get_path_length(end, start)
print(back.t)

back_again = windy_pops.get_path_length(back, end)
print(back_again.t)
