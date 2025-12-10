# cooperative_astar.py
# ---------------------------------------------------------
# Cooperative A* - përdor A* për çdo agjent, duke shmangur
# qelizat e zëna dhe përplasjet në kohë (reservation table)
# ---------------------------------------------------------

from a_star import a_star
import heapq


# ---------------------------------------------------------
# Funksion që ndërton reservation table nga një path
# ---------------------------------------------------------
def reserve_path(res_table, path):
    for t, pos in enumerate(path):
        if t not in res_table:
            res_table[t] = set()
        res_table[t].add(pos)

    # Rezervojmë edhe pozicionin e fundit për shumë timesteps
    # nëse agjentët e tjerë arrijnë më vonë
    last = path[-1]
    for t in range(len(path), len(path) + 50):
        if t not in res_table:
            res_table[t] = set()
        res_table[t].add(last)


# ---------------------------------------------------------
# Kontrollon nëse qeliza është e lirë në një timestep
# ---------------------------------------------------------
def is_reserved(pos, time, res_table):
    return time in res_table and pos in res_table[time]


# ---------------------------------------------------------
# A* për cooperative pathfinding
# ---------------------------------------------------------
def a_star_cooperative(start, goal, grid, res_table):
    open_set = []
    heapq.heappush(open_set, (0, 0, start))  # (f_score, time, node)

    came_from = {}
    g_score = {(start, 0): 0}

    while open_set:
        _, time, current = heapq.heappop(open_set)

        # Nëse arritëm te qëllimi
        if current == goal:
            return reconstruct_coop_path(came_from, (current, time))

        # Fqinjët
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1), (0,0)]:  # kemi edhe "stay still"
            nx, ny = current[0] + dx, current[1] + dy
            next_pos = (nx, ny)
            next_time = time + 1

            # Kufijtë e grid-it
            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                continue

            # Pengesë
            if grid[nx][ny] == 1:
                continue

            # Kontrollo reservation table
            if is_reserved(next_pos, next_time, res_table):
                continue

            # Kontrollo collision edge-to-edge (shkëmbim vendesh)
            if is_reserved(current, next_time, res_table):
                continue

            # Llogarit cost
            new_cost = g_score[(current, time)] + 1

            if (next_pos, next_time) not in g_score or new_cost < g_score[(next_pos, next_time)]:
                came_from[(next_pos, next_time)] = (current, time)
                g_score[(next_pos, next_time)] = new_cost

                f = new_cost + abs(goal[0] - nx) + abs(goal[1] - ny)
                heapq.heappush(open_set, (f, next_time, next_pos))

    return None  # s'ka rrugë


# ---------------------------------------------------------
# Rindërto path-in nga came_from
# ---------------------------------------------------------
def reconstruct_coop_path(came_from, current):
    path = [current[0]]
    while current in came_from:
        current = came_from[current]
        path.append(current[0])
    path.reverse()
    return path


# ---------------------------------------------------------
# Funksioni kryesor: planifikimi për shumë agjentë
# ---------------------------------------------------------
def cooperative_astar(agents, grid):
    """
    agents = [
      {"start": (x,y), "goal": (x,y)},
      {"start": (x,y), "goal": (x,y)}
    ]
    """
    res_table = {}
    paths = []

    for i, agent in enumerate(agents):
        start = agent["start"]
        goal = agent["goal"]

        path = a_star_cooperative(start, goal, grid, res_table)

        if path is None:
            print(f"Agjenti {i} nuk gjeti rrugë!")
            return None

        paths.append(path)
        reserve_path(res_table, path)

    return paths
