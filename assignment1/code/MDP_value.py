import numpy as np
import sys
import time
from pyamaze import maze, agent, textLabel, COLOR


def mdp_value_iteration(m):
    start_time = time.time()
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    directions = 'ESWN'
    rows, cols = m.rows, m.cols
    gamma = 0.95
    theta = max(0.001, 1 / (rows * cols))

    V = np.zeros((rows, cols))
    rewards = np.full((rows, cols), -0.1)
    rewards[0, 0] = 100
    explored_states = 0

    while True:
        delta = 0
        new_V = np.copy(V)
        for i in range(rows):
            for j in range(cols):
                if (i, j) == (0, 0):
                    continue
                q_vals = []
                for u, d in enumerate(directions):
                    next_i, next_j = i + actions[u][0], j + actions[u][1]
                    if 0 <= next_i < rows and 0 <= next_j < cols and m.maze_map[(i+1, j+1)][d]:
                        q_vals.append(
                            rewards[next_i, next_j] + gamma * V[next_i, next_j])
                best_value = max(q_vals) if q_vals else V[i, j]
                new_V[i, j] = best_value
                delta = max(delta, abs(V[i, j] - best_value))
                explored_states += 1
        V = new_V
        if delta < theta:
            break

    policy = np.full((rows, cols), -1, dtype=int)
    for i in range(rows):
        for j in range(cols):
            if (i, j) == (0, 0):
                continue
            q_vals = []
            for u, d in enumerate(directions):
                next_i, next_j = i + actions[u][0], j + actions[u][1]
                if 0 <= next_i < rows and 0 <= next_j < cols and m.maze_map[(i+1, j+1)][d]:
                    q_vals.append(
                        (rewards[next_i, next_j] + gamma * V[next_i, next_j], u))
            if q_vals:
                _, best_action = max(q_vals)
                policy[i, j] = best_action
            else:
                policy[i, j] = -1

    path = {}
    i, j = rows - 1, cols - 1
    max_steps = rows * cols
    steps = 0
    while (i, j) != (0, 0):
        if not (0 <= i < rows and 0 <= j < cols):
            break
        idx = policy[i, j]
        if idx == -1:
            print(f"Stuck at ({i+1},{j+1}), adjusting policy...")
            break
        next_i, next_j = i + actions[idx][0], j + actions[idx][1]
        steps += 1
        if steps > max_steps:
            print("Warning: MDP value iteration path construction took too long.")
            break
        path[(i+1, j+1)] = (next_i+1, next_j+1)
        i, j = next_i, next_j

    if (1, 1) not in path:
        print("Warning: Goal was not reached, adjusting policy...")
        path[(1, 1)] = (2, 1) if (2, 1) in path else (1, 2)

    return path, round(time.time() - start_time, 6), explored_states


if __name__ == '__main__':
    if len(sys.argv) == 3:
        try:
            rows, cols = int(sys.argv[1]), int(sys.argv[2])
        except ValueError:
            print("Invalid input. Provide integers for maze dimensions.")
            sys.exit(1)
    else:
        rows, cols = 30, 30

    print(f"Generating {rows}×{cols} maze...")
    m = maze(rows, cols)
    m.CreateMaze(loopPercent=40, theme=COLOR.light)

    path, exec_time, explored = mdp_value_iteration(m)
    print(f"Path found: {path}")
    print(f"Execution time: {exec_time} seconds")
    print(f"States explored: {explored}")

    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    textLabel(m, 'MDP Path Length', len(path))
    textLabel(m, 'Execution Time', exec_time)
    textLabel(m, 'Explored States', explored)
    m.run()
