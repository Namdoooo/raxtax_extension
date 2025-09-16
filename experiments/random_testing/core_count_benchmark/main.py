from pathlib import Path

from simulator import run_all_main
from metadata_reader import parse_metadata_independent_dependent_variable
from data_generator import create_folder
from viz_utils import plot_xy_data


def visualize():
    root_dir = Path(__file__).resolve().parent
    core_counts, calculate_intersection_sizes_times = parse_metadata_independent_dependent_variable(root_dir, "calculate_intersection_sizes_time")

    result_path = root_dir / "results"
    create_folder(result_path)

    print(core_counts)
    print(calculate_intersection_sizes_times)

    title = "Core Count Benchmark"
    xLabel = "Core Count"
    yLabel = "Calculate Intersection Sizes Time (s)"
    save_path = result_path / "core_counts_benchmark.png"

    plot_xy_data(core_counts, calculate_intersection_sizes_times, title=title, xlabel=xLabel, ylabel=yLabel, save_path=save_path)

if __name__ == "__main__":
    #run_all_main()
    visualize()