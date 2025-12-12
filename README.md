# 33-multi-agent-pathfinding
## 🧭 Përshkrimi

Ky projekt trajton problemin Multi-Agent Pathfinding (MAPF) në një grid 2D, ku një grup agjentësh duhet të lëvizin nga pozicionet fillestare në destinacionet e tyre pa u përplasur.
Zgjidhja mbështetet në:

A* – për gjetjen e rrugëve optimale individuale

Cooperative A* – për koordinimin e shumë agjentëve duke shmangur konfliktet në kohë dhe hapësirë

Vizualizim të Animuar – për të shfaqur lëvizjet e agjentëve dhe rrugët e tyre në mënyrë dinamike

Projekti është i thjeshtë, i modularizuar dhe i zgjerueshëm për përdorime më të avancuara të MAPF.

---

## ⚙️ Algoritmet
A* (a_star.py)
Përdoret për planifikim rrugësh për një agjent të vetëm.
Përdor: lëvizje 4-drejtimshe, heuristikë Manhattan, rindërtim të rrugës përmes came_from.

Cooperative A* (cooperative_astar.py)
Zgjeron A* duke synuar shmangien e konflikteve midis agjentëve. Mekanizmi kyç është struktura Reservations, që ruan: qelizat e rezervuara (vertex conflicts), lëvizjet e rezervuara (edge conflicts)
Kjo siguron që çdo agjent lëviz në mënyrë të sigurt dhe nuk shkëmben pozicione me një agjent tjetër në të njëjtën kohë.

Vizualizimi (visualization.py)
Vizualizimi jep një animacion dinamik, duke shfaqur: pozicionet fillestare (S), destinacionet (rrathët), lëvizjen e agjentëve me interpolim të butë, gjurmët e rrugëve (trail) me ngjyra të ndryshme për çdo agjent, pengesat në grid dhe rrjetin e vizatuar.

---

## 👥 Antarët

- Dituri Kodra
- Nora Morina
- Riga Ferati
---

## 🗂️ Struktura e projektit

```
33-MULTI-AGENT-PATHFINDING/
│
├── a_star.py               # Implementimi i A*
├── cooperative_astar.py    # Implementimi i Cooperative A*
├── visualization.py        # Vizualizimi i animuar i MAPF
├── .gitignore
├── README.md
└── __pycache__/             # File automatike të Python

```

---

![Screen Recording 2025-12-12 at 16 57 11](https://github.com/user-attachments/assets/6a847d51-7644-48d0-8cb3-ef9166de2181)
