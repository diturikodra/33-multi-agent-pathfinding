from cooperative_astar import cooperative_astar

grid = [
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,0,0,0,0]
]

agents = [
    {"start": (0,0), "goal": (2,2)},
    {"start": (0,3), "goal": (0,4)}
]

paths = cooperative_astar(agents, grid)
print(paths)
