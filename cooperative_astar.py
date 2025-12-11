import heapq

class Reservations:

    def __init__(self):
        # time -> set of (row, col)
        self.vertex = {}
        # time -> set of ((from_row, from_col), (to_row, to_col))
        self.edge = {}

    def reserve_vertex(self, pos, t):
        if t not in self.vertex:
            self.vertex[t] = set()
        self.vertex[t].add(pos)

    def is_vertex_reserved(self, pos, t):
        return t in self.vertex and pos in self.vertex[t]

    def reserve_edge(self, from_pos, to_pos, t):
        
        if t not in self.edge:
            self.edge[t] = set()
        self.edge[t].add((from_pos, to_pos))

    def is_edge_conflict(self, from_pos, to_pos, t):
        
        if t not in self.edge:
            return False
        
        return (to_pos, from_pos) in self.edge[t]


    def reserve_path(self, path, extra_goal_horizon=50):

        if not path:
            return

        # vertex + edge 
        for t in range(len(path)):
            pos = path[t]
            self.reserve_vertex(pos, t)
            if t > 0:
                prev = path[t - 1]
                self.reserve_edge(prev, pos, t)

        # goal
        last = path[-1]
        for t in range(len(path), len(path) + extra_goal_horizon):
            self.reserve_vertex(last, t)


def a_star_cooperative(start, goal, grid, reservations, max_time=500):

    # Open list = priority queue me elemente (f_score, time, pos)
    open_set = []
    heapq.heappush(open_set, (0, 0, start))

    came_from = {}
    g_score = {(start, 0): 0}

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while open_set:
        f, time, current = heapq.heappop(open_set)

        if time > max_time:
            continue

        if current == goal:
            return reconstruct_coop_path(came_from, (current, time))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            next_pos = (nx, ny)
            next_time = time + 1

            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                continue

            if grid[nx][ny] == 1:
                continue

            if reservations.is_vertex_reserved(next_pos, next_time):
                continue

            if reservations.is_edge_conflict(current, next_pos, next_time):
                continue

            new_cost = g_score[(current, time)] + 1
            neighbor_state = (next_pos, next_time)

            if (next_pos, next_time) not in g_score or new_cost < g_score[neighbor_state]:
                g_score[neighbor_state] = new_cost
                came_from[neighbor_state] = (current, time)

                f_score = new_cost + heuristic(next_pos, goal)
                heapq.heappush(open_set, (f_score, next_time, next_pos))

    return None


def reconstruct_coop_path(came_from, current_state):
    pos, time = current_state
    path = [pos]

    while current_state in came_from:
        current_state = came_from[current_state]
        path.append(current_state[0])

    path.reverse()
    return path

def cooperative_astar(agents, grid):
    """
    agents = [
        {"start": (x, y), "goal": (x, y)},
        {"start": (x, y), "goal": (x, y)},
        ...
    ]

    returns:
        paths = [
            [(r0, c0), (r1, c1), ...],  # agent 0
            [(r0, c0), (r1, c1), ...],  # agent 1
            ...
        ]
    """

    reservations = Reservations()
    paths = []

    for i, agent in enumerate(agents):
        start = agent["start"]
        goal = agent["goal"]

        path = a_star_cooperative(start, goal, grid, reservations)

        if path is None:
            print(f"Agjenti {i} nuk gjeti rrugë!")
            return None

        paths.append(path)
        reservations.reserve_path(path)

    return paths
