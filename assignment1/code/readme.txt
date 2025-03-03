Maze Solving Algorithms - Console Interface
============================================

This package contains implementations of various maze solving algorithms:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- A* Search
- MDP Value Iteration
- MDP Policy Iteration

The file "run_console.py" provides a simple console interface to run any of these algorithms on a generated maze.

Requirements:
-------------
- Python 3.x
- Required packages: pyamaze, numpy, matplotlib, argparse
  (Install them via pip if not already installed, for example:
   pip install pyamaze numpy matplotlib)

How to Run:
-----------
Open your terminal or command prompt and navigate to the directory containing the files.

Use the following command format to run an algorithm:

    python run_console.py --algorithm [ALGORITHM] --rows [ROWS] --cols [COLS] [--visualize]

Parameters:
-----------
--algorithm  : The algorithm to use. Choose from:
              bfs, dfs, astar, mdp_value, mdp_policy
--rows       : (Optional) Number of rows for the maze. Default is 30.
--cols       : (Optional) Number of columns for the maze. Default is 30.
--visualize  : (Optional) Include this flag to display the maze and solution path graphically.

Examples:
---------
1. Run A* algorithm on a 20x20 maze with visualization:
   python run_console.py --algorithm astar --rows 20 --cols 20 --visualize

2. Run BFS algorithm on a default 30x30 maze without visualization:
   python run_console.py --algorithm bfs

3. Run DFS algorithm on a 50x50 maze:
   python run_console.py --algorithm dfs --rows 50 --cols 50

Output:
-------
The program will print:
- Maze dimensions and algorithm details.
- Execution time, states explored, and path length.
- The computed solution path.
If the --visualize flag is provided, a graphical window will open showing the maze with the solution traced.

Troubleshooting:
----------------
- Ensure all required packages are installed.
- Verify you have typed the algorithm name correctly.
- For issues with visualization, make sure your environment supports graphical display.
