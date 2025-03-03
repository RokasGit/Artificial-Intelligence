import argparse
import time
from pyamaze import maze, agent, textLabel, COLOR
from astar import astar_algorithm
from bfs import bfs_algorithm
from dfs import dfs_algorithm
from MDP_policy import mdp_policy_iteration
from MDP_value import mdp_value_iteration


def main():
    parser = argparse.ArgumentParser(
        description="Maze Solving Algorithms Console Interface")
    parser.add_argument("-a", "--algorithm", type=str, required=True,
                        choices=["bfs", "dfs", "astar",
                                 "mdp_value", "mdp_policy"],
                        help="Algorithm to use: bfs, dfs, astar, mdp_value, mdp_policy")
    parser.add_argument("-r", "--rows", type=int, default=30,
                        help="Number of rows in the maze (default: 30)")
    parser.add_argument("-c", "--cols", type=int, default=30,
                        help="Number of columns in the maze (default: 30)")
    parser.add_argument("-v", "--visualize", action="store_true",
                        help="Visualize the maze and solution path")
    args = parser.parse_args()

    algorithms = {
        "bfs": bfs_algorithm,
        "dfs": dfs_algorithm,
        "astar": astar_algorithm,
        "mdp_value": mdp_value_iteration,
        "mdp_policy": mdp_policy_iteration
    }

    selected_algo = algorithms[args.algorithm]

    print(f"Generating a {args.rows}x{args.cols} maze...")
    m = maze(args.rows, args.cols)
    m.CreateMaze(loopPercent=40, theme=COLOR.light)

    print(f"Running {args.algorithm} algorithm...")
    result = selected_algo(m)
    if len(result) == 3:
        path, exec_time, explored = result
    else:
        path, exec_time = result
        explored = len(path) if path else 0

    print("\n--- Algorithm Results ---")
    print(f"Algorithm: {args.algorithm}")
    print(f"Execution Time: {exec_time} seconds")
    print(f"States Explored: {explored}")
    print(f"Path Length: {len(path)}")
    print("Path:", path)

    if args.visualize:
        a = agent(m, footprints=True, filled=True)
        m.tracePath({a: path})
        textLabel(m, 'Path Length', len(path) + 1)
        textLabel(m, 'Execution Time', exec_time)
        textLabel(m, 'States Explored', explored)
        m.run()
    else:
        print("Visualization disabled. Run with --visualize flag to see the maze.")


if __name__ == "__main__":
    main()
