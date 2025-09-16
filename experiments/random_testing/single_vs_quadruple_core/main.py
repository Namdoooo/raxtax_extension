from distutils.command.install_egg_info import safe_version
from pathlib import Path

from simulator import run_all_main
from metadata_reader import parse_metadata_independent_dependent_variable
from data_generator import create_folder
from viz_utils import plot_multiple_xy_array


def visualize():
    root_dir = Path(__file__).resolve().parent

    root_quadruple_dir = root_dir / "quadruple"
    root_single_dir = root_dir / "single"

    test_nums1, calculate_intersection_sizes_times_single = parse_metadata_independent_dependent_variable(root_single_dir, "calculate_intersection_sizes_time")
    test_nums2, calculate_intersection_sizes_times_quadruple = parse_metadata_independent_dependent_variable(root_quadruple_dir, "calculate_intersection_sizes_time")

    result_path = root_dir / "results"
    create_folder(result_path)

    x_data = [test_nums1, test_nums2]
    y_data = [calculate_intersection_sizes_times_single, calculate_intersection_sizes_times_quadruple]

    title = "Single vs Quadruple Core Performance"
    xlabel = "Test Number"
    ylabel = "Calculate Intersection Sizes Time"


    save_path = result_path / "single_vs_quadruple_core.png"

    plot_multiple_xy_array(x_data, y_data, title=title, xlabel=xlabel, ylabel=ylabel, save_path=save_path)

if __name__ == "__main__":
    #run_all_main()
    visualize()