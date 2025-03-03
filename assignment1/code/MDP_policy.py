from pyamaze import maze, agent, textLabel, COLOR
import numpy as np
import time
import sys


def mdp_policy_iteration(m):
    start_time = time.time()
    directions = 'ESWN'
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    rows, cols = m.rows, m.cols
    gamma = 0.9
    theta = 0.001

    V = np.zeros((rows, cols))
    policy = np.random.choice(len(actions), size=(rows, cols))
    rewards = np.full((rows, cols), -1.0)
    rewards[0, 0] = 100

    explored_states = 0
    stable_policy = False
    while not stable_policy:
        while True:
            delta = 0
            new_V = np.copy(V)
            for i in range(rows):
                for j in range(cols):
                    if (i, j) == (0, 0):
                        continue
                    u = policy[i, j]
                    next_i, next_j = i + actions[u][0], j + actions[u][1]
                    if 0 <= next_i < rows and 0 <= next_j < cols and m.maze_map[(i+1, j+1)][directions[u]]:
                        value = rewards[next_i, next_j] + \
                            gamma * V[next_i, next_j]
                    else:
                        value = V[i, j]
                    new_V[i, j] = value
                    delta = max(delta, abs(V[i, j] - value))
                    explored_states += 1
            V = new_V
            if delta < theta:
                break

        stable_policy = True
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
                    best_value, best_action = max(q_vals)
                    if best_action != policy[i, j]:
                        stable_policy = False
                        policy[i, j] = best_action

    path = {}
    i, j = rows - 1, cols - 1
    max_steps = rows * cols
    steps = 0
    while (i, j) != (0, 0):
        if not (0 <= i < rows and 0 <= j < cols):
            break
        idx = policy[i, j]
        next_i, next_j = i + actions[idx][0], j + actions[idx][1]
        steps += 1
        if steps > max_steps:
            print(
                "Warning: MDP policy iteration path construction exceeded maximum steps.")
            break
        path[(i+1, j+1)] = (next_i+1, next_j+1)
        i, j = next_i, next_j

    return path, round(time.time() - start_time, 6), explored_states


if __name__ == '__main__':
    if len(sys.argv) == 3:
        try:
            rows, cols = int(sys.argv[1]), int(sys.argv[2])
        except ValueError:
            print("Invalid input. Provide integers for maze size.")
            sys.exit(1)
    else:
        rows, cols = 20, 20

    print(f"Generating {rows}×{cols} maze...")
    m = maze(rows, cols)
    m.CreateMaze(loopPercent=40, theme=COLOR.light)

    path, exec_time, explored = mdp_policy_iteration(m)
    print(f"Path found: {path}")
    print(f"Execution time: {exec_time} seconds")
    print(f"States explored: {explored}")

    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    textLabel(m, 'MDP Path Length', len(path))
    textLabel(m, 'Execution Time', exec_time)
    textLabel(m, 'States Explored', explored)
    m.run()
