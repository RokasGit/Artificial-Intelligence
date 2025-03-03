import sys
import time
from collections import deque
from pyamaze import maze, agent, textLabel, COLOR


def dfs_algorithm(m):
    start_time = time.time()
    directions = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)}
    destination, start = (1, 1), (m.rows, m.cols)
    stack = deque([start])
    visited = {start}
    path = {}
    explored_states = 0

    while stack:
        current = stack.pop()
        explored_states += 1
        if current == destination:
            break
        for d, (dx, dy) in directions.items():
            if m.maze_map[current][d]:
                nxt = (current[0] + dx, current[1] + dy)
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append(nxt)
                    path[nxt] = current

    dfs_path = {}
    current = destination
    while current in path:
        dfs_path[path[current]] = current
        current = path[current]

    return dfs_path, round(time.time() - start_time, 6), explored_states


if __name__ == '__main__':
    if len(sys.argv) == 3:
        try:
            rows, cols = int(sys.argv[1]), int(sys.argv[2])
        except ValueError:
            print("Invalid input. Please provide integers for maze dimensions.")
            sys.exit(1)
    else:
        rows, cols = 30, 30

    print(f"Generating {rows}×{cols} maze...")
    m = maze(rows, cols)
    m.CreateMaze(loopPercent=40, theme=COLOR.light)

    path, exec_time, explored = dfs_algorithm(m)
    print(f"Path found: {path}")
    print(f"Execution time: {exec_time} seconds")
    print(f"States explored: {explored}")

    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    textLabel(m, 'Path Length', len(path) + 1)
    textLabel(m, 'Execution Time', exec_time)
    textLabel(m, 'States Explored', explored)
    m.run()
