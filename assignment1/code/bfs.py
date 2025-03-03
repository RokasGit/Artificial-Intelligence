import sys
import time
from collections import deque
from pyamaze import maze, agent, textLabel, COLOR


def bfs_algorithm(m):
    start_time = time.time()
    directions = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)}
    destination = (1, 1)
    start = (m.rows, m.cols)

    queue = deque([start])
    visited = set([start])
    path = {}
    explored_states = 0

    while queue:
        current = queue.popleft()
        explored_states += 1
        if current == destination:
            break
        for d, (dx, dy) in directions.items():
            if m.maze_map[current][d]:
                nxt = (current[0] + dx, current[1] + dy)
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
                    path[nxt] = current

    bfs_path = {}
    current = destination
    while current in path:
        bfs_path[path[current]] = current
        current = path[current]

    return bfs_path, round(time.time() - start_time, 6), explored_states


if __name__ == '__main__':
    if len(sys.argv) == 3:
        try:
            rows = int(sys.argv[1])
            cols = int(sys.argv[2])
        except ValueError:
            print("Invalid input. Provide integers for rows and columns.")
            sys.exit(1)
    else:
        rows, cols = 30, 30

    print(f"Generating {rows}×{cols} maze...")
    m = maze(rows, cols)
    m.CreateMaze(loopPercent=40, theme=COLOR.light)

    path, exec_time, explored = bfs_algorithm(m)
    print(f"Path found: {path}")
    print(f"Execution time: {exec_time} seconds")
    print(f"States explored: {explored}")

    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    textLabel(m, 'Path Length', len(path) + 1)
    textLabel(m, 'Execution Time', exec_time)
    textLabel(m, 'States Explored', explored)
    m.run()
