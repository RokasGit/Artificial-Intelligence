import sys
import time
import heapq
from collections import defaultdict
from pyamaze import maze, agent, textLabel, COLOR


def heuristic(cur, goal):
    return abs(cur[0] - goal[0]) + abs(cur[1] - goal[1])


def astar_algorithm(m):
    start_time = time.time()
    directions = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)}
    start, goal = (m.rows, m.cols), (1, 1)

    g_score = defaultdict(lambda: float('inf'))
    f_score = defaultdict(lambda: float('inf'))
    g_score[start], f_score[start] = 0, heuristic(start, goal)

    open_set = []
    heapq.heappush(open_set, (f_score[start], heuristic(start, goal), start))
    path, visited = {}, set()
    explored_states = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        explored_states += 1
        if current == goal:
            break
        for d, (dx, dy) in directions.items():
            if m.maze_map[current][d]:
                nxt = (current[0] + dx, current[1] + dy)
                if nxt in visited:
                    continue
                tentative_g = g_score[current] + 1
                if tentative_g < g_score[nxt]:
                    g_score[nxt] = tentative_g
                    f_score[nxt] = tentative_g + heuristic(nxt, goal)
                    heapq.heappush(
                        open_set, (f_score[nxt], heuristic(nxt, goal), nxt))
                    path[nxt] = current

    astar_path = {}
    current = goal
    while current in path:
        astar_path[path[current]] = current
        current = path[current]

    return astar_path, round(time.time() - start_time, 6), explored_states


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

    path, exec_time, explored = astar_algorithm(m)
    print(f"Path found: {path}")
    print(f"Execution time: {exec_time} seconds")
    print(f"States explored: {explored}")

    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    textLabel(m, 'A* Path Length', len(path) + 1)
    textLabel(m, 'Execution Time', exec_time)
    textLabel(m, 'States Explored', explored)
    m.run()
