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
    {"start": (6, 0), "goal": (0, 0)},
    {"start": (6, 2), "goal": (2, 3)}

]

paths = cooperative_astar(agents, grid)

if paths is None:
    print("Nuk mund të gjenin rrugë për të gjithë agjentët!")
    exit()

max_len = max(len(path) for path in paths)

for path in paths:
    last = path[-1]
    while len(path) < max_len:
        path.append(last)



agents_paths = {f'Agent{i}': path for i, path in enumerate(paths)}
colors = {'Agent0': 'blue', 'Agent1': 'red', 'Agent2': 'green', 'Agent3': 'orange', 'Agent4': 'purple', 'Agent5': 'cyan', 'Agent6': 'magenta', 'Agent7': 'yellow','Agent8': 'brown'}

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
    
for i, agent_data in enumerate(agents):
    agent_id = f'Agent{i}'
    color = colors[agent_id]
    
    # Start Point (S)
    start_r, start_c = agent_data["start"]
    ax.text(start_c, start_r, 'S', color=color, fontsize=12, fontweight='bold', ha='center', va='center')
    
    # Goal Point (Vijë Rrethore)
    goal_r, goal_c = agent_data["goal"]
    ax.plot(
        [goal_c], 
        [goal_r], 
        marker='o',  # Rreth (Circle)
        markersize=16, 
        linestyle='',
        markeredgecolor=color, 
        markeredgewidth=2,     
        markerfacecolor='none' 
    )
    

markers = {}
trails = {} 

# Inicializimi i Agjentëve dhe Vijave të Hijezimit
for agent, path in agents_paths.items():
    r, c = path[0]
    # Agjenti (zorder=3 për të qenë sipër gjurmës)
    marker, = ax.plot([c], [r], 'o', color=colors[agent], markersize=15, zorder=3)
    markers[agent] = marker
    
    # Inicializimi i vijës së hijezimit (trail), fillimisht bosh
    # Vija (zorder=2 për të qenë prapa agjentit)
    trail, = ax.plot([], [], color=colors[agent], linewidth=2, linestyle='-', zorder=2, alpha=0.5)
    trails[agent] = trail

SUBSTEPS = 10

max_segments = max(len(p) - 1 for p in agents_paths.values())

# Buffer kohor: siguron që vija e hijezimit të mbetet për pak kohë para se të fshihet
total_frames = max_segments * SUBSTEPS + SUBSTEPS * 10 


def interpolate(p0, p1, alpha):
    # linear: p = p0 + alpha * (p1 - p0)
    (r0, c0), (r1, c1) = p0, p1
    r = r0 + (r1 - r0) * alpha
    c = c0 + (c1 - c0) * alpha
    return r, c


def update(frame):
    # frame: 0 .. total_frames-1
    changed_artists = [] 
    
    for agent, path in agents_paths.items():

        segments = len(path) - 1
        
        # Segmenti ku ndodhemi (indexi i rrugës)
        seg_idx = frame // SUBSTEPS
        
        # Vlera interpoluese brenda segmentit
        alpha = (frame % SUBSTEPS) / SUBSTEPS

        # Llogaritja e pozicionit aktual (interpoluar)
        if seg_idx >= segments:
            # Agjenti ka arritur në destinacion, mbetet në vendin e fundit
            r, c = path[-1]
            
        else:
            # Agjenti është duke lëvizur
            p0 = path[seg_idx]
            p1 = path[seg_idx + 1]
            r, c = interpolate(p0, p1, alpha)
        
        markers[agent].set_data([c], [r])
        changed_artists.append(markers[agent]) 

        
        # LOGJIKA E VIJËS SË HIJEZIMIT (TRAIL)
        if seg_idx < segments:
            # Agjenti është duke lëvizur: vizatojmë path-in e plotë deri në pikën aktuale
            
            # Pikat e kaluara (koordinatat e qendrës së qelizave)
            trail_r = [p[0] for p in path[:seg_idx + 1]]
            trail_c = [p[1] for p in path[:seg_idx + 1]]
            
            # Pozicioni aktual (koordinatat e interpoluara)
            trail_r.append(r)
            trail_c.append(c)
            
            trails[agent].set_data(trail_c, trail_r)
        
        elif seg_idx >= segments and frame <= max_segments * SUBSTEPS:
             # Agjenti ka arritur, vija mbetet e plotë në destinacion gjatë kohës së buffer-it
             trail_r = [p[0] for p in path]
             trail_c = [p[1] for p in path]
             trails[agent].set_data(trail_c, trail_r)
             
        elif frame > max_segments * SUBSTEPS:
            # Pas kohës së buffer-it, vija hiqet
            trails[agent].set_data([], [])

        changed_artists.append(trails[agent]) 
    # Kthehen të gjithë artistët e ndryshuar (kërkohet nga blit=True)
    return changed_artists 


ani = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    interval=50,
    blit=True,     # Përdorim blit=True për performancë më të mirë me gjurmët (trails)
    repeat=True   # Ndalon animacionin pasi të ketë mbaruar
)

plt.show()