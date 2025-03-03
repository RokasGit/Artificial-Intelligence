import pandas as pd
import matplotlib.pyplot as plt
import os


def main():
    df = pd.read_csv("algorithm_performance.csv")

    df["Maze Size"] = df["Maze Size"].apply(lambda x: int(x.split('x')[0]))

    if not os.path.exists("analysis_plots"):
        os.makedirs("analysis_plots")

    plt.figure(figsize=(8, 6))
    for algo in df["Algorithm"].unique():
        subset = df[df["Algorithm"] == algo]
        plt.errorbar(
            subset["Maze Size"],
            subset["Time (s)"],
            yerr=subset.groupby("Maze Size")["Time (s)"].std().values,
            marker="o", label=algo, capsize=5
        )
    plt.xlabel("Maze Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time vs. Maze Size")
    plt.legend()
    plt.savefig("analysis_plots/execution_time.png")

    plt.figure(figsize=(8, 6))
    for algo in df["Algorithm"].unique():
        subset = df[df["Algorithm"] == algo]
        plt.errorbar(
            subset["Maze Size"],
            subset["States Explored"],
            yerr=subset.groupby("Maze Size")["States Explored"].std().values,
            marker="s", label=algo, capsize=5
        )
    plt.xlabel("Maze Size")
    plt.ylabel("States Explored")
    plt.title("States Explored vs. Maze Size")
    plt.legend()
    plt.savefig("analysis_plots/states_explored.png")

    plt.figure(figsize=(8, 6))
    for algo in df["Algorithm"].unique():
        subset = df[df["Algorithm"] == algo]
        plt.errorbar(
            subset["Maze Size"],
            subset["Path Length"],
            yerr=subset.groupby("Maze Size")["Path Length"].std().values,
            marker="^", label=algo, capsize=5
        )
    plt.xlabel("Maze Size")
    plt.ylabel("Path Length")
    plt.title("Path Length vs. Maze Size")
    plt.legend()
    plt.savefig("analysis_plots/path_length.png")

    print("\nPerformance graphs saved in 'analysis_plots/'")

    summary = df.groupby("Algorithm").agg({
        "Time (s)": ["mean", "std"],
        "States Explored": ["mean", "std"],
        "Path Length": ["mean", "std"],
        "Success": ["mean"]
    })
    summary.to_csv("analysis_plots/summary_statistics.csv")
    print("\nSummary Statistics:")
    print(summary)


if __name__ == "__main__":
    main()
