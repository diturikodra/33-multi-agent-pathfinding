# a_star.py
# ---------------------------------------------------------
# Implementim i pastër i A* për një agjent në një grid 2D.
# ---------------------------------------------------------

import heapq

# Heuristika: Manhattan distance (përshtatshme për grid 4-directional)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Merr fqinjët validë (lëvizje lart, poshtë, majtas, djathtas)
def get_neighbors(node, grid):
    neighbors = []
    x, y = node
    directions = [(1,0), (-1,0), (0,1), (0,-1)]  # 4-directional movement

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        # Kontrollo kufijtë e grid-it
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            # 0 = qelizë e lirë, 1 = pengesë
            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))

    return neighbors


# ---------------------------------------------------------
# A* algorithm
# ---------------------------------------------------------
def a_star(start, goal, grid):
    # Open list = priority queue (heap)
    open_set = []
    heapq.heappush(open_set, (0, start))

    # Mban nga erdhi çdo nodë
    came_from = {}

    # G-cost = kostoja e distancës nga start-i
    g_score = {start: 0}

    # F-cost = g + heuristikë
    f_score = {start: heuristic(start, goal)}

    while open_set:
        # Nxjerrim nodën me f-score më të ulët
        current = heapq.heappop(open_set)[1]

        # Nëse e kemi arritur qëllimin, rindërtojmë path-in
        if current == goal:
            return reconstruct_path(came_from, current)

        # Fqinjët
        for neighbor in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1  # çdo lëvizje kushton 1

            # Nëse g është më i mirë (më i shkurtër)
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)

                # Shtoje fqinjin në open_set
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # Nëse nuk gjejmë rrugë
    return None


# ---------------------------------------------------------
# Funksion ndihmës që rindërton rrugën nga came_from[]
# ---------------------------------------------------------
def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


# ---------------------------------------------------------
# Test i thjeshtë (mund ta fshish)
# ---------------------------------------------------------
if __name__ == "__main__":

    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    start = (0, 0)
    goal = (2, 4)

    path = a_star(start, goal, grid)
    print("Path:", path)
