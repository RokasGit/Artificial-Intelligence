import time
import tracemalloc
import csv
from pyamaze import maze, agent, COLOR
from MDP_policy import mdp_policy_iteration
from MDP_value import mdp_value_iteration
from astar import astar_algorithm
from bfs import bfs_algorithm
from dfs import dfs_algorithm


def run_and_log_algorithm(algorithm, maze_obj, algorithm_name, maze_size):
    tracemalloc.start()
    start_time = time.perf_counter()
    result = algorithm(maze_obj)
    if len(result) == 3:
        path, exec_time, explored_states = result
    else:
        path, exec_time = result
        explored_states = len(path) if path else 0
    overall_time = time.perf_counter() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak / 1024

    path_length = len(path) if path else -1
    success = 1 if path else 0

    with open("algorithm_performance.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            algorithm_name, f"{maze_size[0]}x{maze_size[1]}",
            round(overall_time, 6), explored_states, path_length, success, round(
                peak_kb, 2)
        ])
    return path


def main():
    algorithms = {
        "BFS": bfs_algorithm,
        "DFS": dfs_algorithm,
        "A*": astar_algorithm,
        "MDP Value Iteration": mdp_value_iteration,
        "MDP Policy Iteration": mdp_policy_iteration
    }

    maze_sizes = [(10, 10), (20, 20), (30, 30), (50, 50), (100, 100)]
    csv_filename = "algorithm_performance.csv"

    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Maze Size", "Time (s)",
                        "States Explored", "Path Length", "Success", "Memory Usage (KB)"])

    for size in maze_sizes:
        rows, cols = size
        print(f"Generating {rows}×{cols} maze...")
        m = maze(rows, cols)
        m.CreateMaze(loopPercent=40, theme=COLOR.light)
        for name, algo in algorithms.items():
            print(f"Running {name} on {rows}×{cols} maze...")
            path = run_and_log_algorithm(algo, m, name, size)
            a = agent(m, footprints=True, filled=True)
            m.tracePath({a: path})
            time.sleep(1)
    print(f"\nAll experiments completed. Results saved in {csv_filename}")


if __name__ == "__main__":
    main()
