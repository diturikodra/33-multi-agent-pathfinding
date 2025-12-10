# ---------------------------------------------------------
# Shembull i plotë: Cooperative A* + Vizualizim
# ---------------------------------------------------------

from cooperative_astar import cooperative_astar
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# ---------------------------------
# Grid dhe pengesa
# 0 = qelizë e lirë
# 1 = pengesë
# ---------------------------------
rows, cols = 5, 5
grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

# Lista e pengesave për vizualizim
obstacles = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]

# ---------------------------------
# Definimi i agjentëve
# ---------------------------------
agents = [
    {"start": (0,0), "goal": (2,4)},
    {"start": (4,4), "goal": (0,2)},
    {"start": (2,1), "goal": (0,1)},
    {"start": (0,1), "goal": (1,1)}
]

# Planifikimi i rrugëve
paths = cooperative_astar(agents, grid)

if paths is None:
    print("Nuk mund të gjenin rrugë për të gjithë agjentët!")
    exit()

# Për vizualizim, krijojmë dictionary me emra dhe paths
agents_paths = {f'Agent{i}': path for i, path in enumerate(paths)}
colors = {'Agent0': 'blue', 'Agent1': 'red','Agent2':'green','Agent3':'pink'}

# ---------------------------------
# Vizualizimi me matplotlib
# ---------------------------------
fig, ax = plt.subplots()
ax.set_xlim(-0.5, cols-0.5)
ax.set_ylim(-0.5, rows-0.5)
ax.set_xticks(range(cols))
ax.set_yticks(range(rows))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(True)

# Shtojmë pengesat
for (r, c) in obstacles:
    rect = patches.Rectangle((c-0.5, r-0.5), 1, 1, color='black')
    ax.add_patch(rect)

# Shtojmë agjentët
markers = {}
for agent, path in agents_paths.items():
    r, c = path[0]
    marker, = ax.plot([c], [r], 'o', color=colors[agent], markersize=15)
    markers[agent] = marker

max_steps = max(len(p) for p in agents_paths.values())

# Funksioni për animacion
def update(frame):
    for agent, path in agents_paths.items():
        if frame < len(path):
            r, c = path[frame]
            markers[agent].set_data([c], [r])  # vendosim koordinatat brenda listës
    return list(markers.values())

ani = FuncAnimation(fig, update, frames=max_steps, interval=500, blit=False, repeat=True)

plt.show()
