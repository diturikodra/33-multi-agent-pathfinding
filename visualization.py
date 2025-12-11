from cooperative_astar import cooperative_astar
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# Grid dhe pengesa
    # 0 = qelizë e lirë
    # 1 = pengesë

rows, cols = 7, 5
grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1]
]

obstacles = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1]

agents = [
    {"start": (0, 0), "goal": (2, 4)},
    {"start": (4, 4), "goal": (0, 2)},
    {"start": (2, 1), "goal": (0, 1)},
    {"start": (1, 1), "goal": (4, 4)},
    {"start": (3, 0), "goal": (0, 4)},
    {"start": (0, 4), "goal": (4, 0)},
    {"start": (4, 0), "goal": (3, 4)},
    {"start": (2, 2), "goal": (4, 2)},
    {"start": (6, 0), "goal": (0, 0)}

]

paths = cooperative_astar(agents, grid)

if paths is None:
    print("Nuk mund të gjenin rrugë për të gjithë agjentët!")
    exit()

agents_paths = {f'Agent{i}': path for i, path in enumerate(paths)}
colors = {'Agent0': 'blue', 'Agent1': 'red', 'Agent2': 'green', 'Agent3': 'orange', 'Agent4': 'purple', 'Agent5': 'cyan', 'Agent6': 'magenta', 'Agent7': 'yellow', 'Agent8': 'brown'}

fig, ax = plt.subplots()
ax.set_xlim(-0.5, cols - 0.5)
ax.set_ylim(-0.5, rows - 0.5)
ax.set_xticks(range(cols))
ax.set_yticks(range(rows))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(True)

for (r, c) in obstacles:
    rect = patches.Rectangle((c - 0.5, r - 0.5), 1, 1, color='black')
    ax.add_patch(rect)

markers = {}
for agent, path in agents_paths.items():
    r, c = path[0]
    marker, = ax.plot([c], [r], 'o', color=colors[agent], markersize=15)
    markers[agent] = marker

SUBSTEPS = 10

max_segments = max(len(p) - 1 for p in agents_paths.values())

total_frames = max_segments * SUBSTEPS + 1


def interpolate(p0, p1, alpha):
    # linear: p = p0 + alpha * (p1 - p0)
    (r0, c0), (r1, c1) = p0, p1
    r = r0 + (r1 - r0) * alpha
    c = c0 + (c1 - c0) * alpha
    return r, c


def update(frame):
    # frame: 0 .. total_frames-1
    for agent, path in agents_paths.items():

        segments = len(path) - 1
        if segments <= 0:

            r, c = path[0]
            markers[agent].set_data([c], [r])
            continue

        seg_idx = frame // SUBSTEPS

        if seg_idx >= segments:
            r, c = path[-1]
            markers[agent].set_data([c], [r])
            continue

        alpha = (frame % SUBSTEPS) / SUBSTEPS

        p0 = path[seg_idx]
        p1 = path[seg_idx + 1]
        r, c = interpolate(p0, p1, alpha)
        markers[agent].set_data([c], [r])

    return list(markers.values())


ani = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    interval=50,
    blit=False,
    repeat=True
)

plt.show()
