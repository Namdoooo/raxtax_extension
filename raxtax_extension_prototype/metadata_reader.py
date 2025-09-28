import os
import re
from pathlib import Path

import numpy as np

import raxtax_extension_prototype.viz_utils as viz_utils
import raxtax_extension_prototype.utils as utils


def read_metadata_mutation_rate_boundary(root_dir: Path):
    metadata = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "metadata.out" in filenames:
            content = {}
            metadata_path = os.path.join(dirpath, "metadata.out")
            with open(metadata_path, "r") as f:
                for line in f:
                    key, value = line.split(": ")
                    content[key.strip()] = value.strip()
            mutation_rate = int(dirpath.split("error")[-1]) / 100
            metadata[mutation_rate] = content
    return metadata

def get_mutation_rate_boundary_results(root_dir: Path):
    mutation_rate_metadata_dic = read_metadata_mutation_rate_boundary(root_dir)

    mutation_rates = []

    calculate_intersection_sizes_times = []

    tps = []
    mcs = []
    fps = []
    fns = []

    recalls = []
    precisions = []
    f1s = []

    for mutation_rate in sorted(mutation_rate_metadata_dic.keys()):
        mutation_rates.append(mutation_rate)

        calculate_intersection_sizes_times.append(float(mutation_rate_metadata_dic[mutation_rate]["calculate_intersection_sizes_time"]))

        tps.append(int(mutation_rate_metadata_dic[mutation_rate]["tp"]))
        mcs.append(int(mutation_rate_metadata_dic[mutation_rate]["mc"]))
        fps.append(int(mutation_rate_metadata_dic[mutation_rate]["fp"]))
        fns.append(int(mutation_rate_metadata_dic[mutation_rate]["fn"]))

        recalls.append(float(mutation_rate_metadata_dic[mutation_rate]["recall"]))
        precisions.append(float(mutation_rate_metadata_dic[mutation_rate]["precision"]))
        f1s.append(float(mutation_rate_metadata_dic[mutation_rate]["f1_score"]))

    result_path = root_dir / "results"

    save_path_calculate_intersection_sizes_times = result_path / "mutation_rate_vs_calculate_intersection_sizes_times.png"

    save_path_tps = result_path / "mutation_rate_vs_tps.png"
    save_path_mcs = result_path / "mutation_rate_vs_mcs.png"
    save_path_fps = result_path / "mutation_rate_vs_fps.png"
    save_path_fns = result_path / "mutation_rate_vs_fns.png"

    save_path_recalls = result_path / "mutation_rate_vs_recalls.png"
    save_path_precisions = result_path / "mutation_rate_vs_precisions.png"
    save_path_f1s = result_path / "mutation_rate_vs_f1s.png"

    viz_utils.plot_xy_data(mutation_rates, calculate_intersection_sizes_times, "Mutation Rate vs Calculate Intersection Sizes Times", "Mutation Rate (%)", "Calculate Intersections Sizes Time (s)", "lines", save_path_calculate_intersection_sizes_times)

    viz_utils.plot_xy_data(mutation_rates, tps, "Mutation Rate vs True Positive Count", "Mutation Rate (%)", "True Positive Count", "lines", save_path_tps)
    viz_utils.plot_xy_data(mutation_rates, mcs, "Mutation Rate vs Misclassified Count", "Mutation Rate (%)", "Misclassified Count", "lines", save_path_mcs)
    viz_utils.plot_xy_data(mutation_rates, fps, "Mutation Rate vs False Positive Count", "Mutation Rate (%)", "False Positive Count", "lines", save_path_fps)
    viz_utils.plot_xy_data(mutation_rates, fns, "Mutation Rate vs False Negative Count", "Mutation Rate (%)", "False Negative Count", "lines", save_path_fns)

    viz_utils.plot_xy_data(mutation_rates, recalls, "Mutation Rate vs Recall", "Mutation Rate (%)", "Recall (%)", "lines", save_path_recalls)
    viz_utils.plot_xy_data(mutation_rates, precisions, "Mutation Rate vs Precision", "Mutation Rate (%)", "Precision (%)", "lines", save_path_precisions)
    viz_utils.plot_xy_data(mutation_rates, f1s, "Mutation Rate vs F1 Score", "Mutation Rate (%)", "F1 Score (%)", "lines", save_path_f1s)

def read_metadata_tree_height_boundary(root_dir: Path):
    metadata = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "metadata.out" in filenames:
            content = {}
            metadata_path = os.path.join(dirpath, "metadata.out")
            with open(metadata_path, "r") as f:
                for line in f:
                    key, value = line.split(": ")
                    content[key.strip()] = value.strip()

            match = re.match(r"t(0*)(\d+)", dirpath.split("/")[-2])
            if match:
                leading_zeros, digits = match.groups()
                if leading_zeros:
                    # Interpret as decimal with as many digits as leading zeros
                    tree_height = float("0." + "0" * (len(leading_zeros) - 1) + digits)
                else:
                    # No leading zeros → whole number
                    tree_height = float(digits)

            metadata[tree_height] = content

    return metadata

def get_tree_height_boundary_results(root_dir: Path):
    tree_height_metadata_dic = read_metadata_tree_height_boundary(root_dir)

    tree_heights = []

    calculate_intersection_sizes_times = []

    tps = []
    mcs = []
    fps = []
    fns = []

    recalls = []
    precisions = []
    f1s = []

    for mutation_rate in sorted(tree_height_metadata_dic.keys()):
        tree_heights.append(mutation_rate)
        calculate_intersection_sizes_times.append(float(tree_height_metadata_dic[mutation_rate]["calculate_intersection_sizes_time"]))

        tps.append(int(tree_height_metadata_dic[mutation_rate]["tp"]))
        mcs.append(int(tree_height_metadata_dic[mutation_rate]["mc"]))
        fps.append(int(tree_height_metadata_dic[mutation_rate]["fp"]))
        fns.append(int(tree_height_metadata_dic[mutation_rate]["fn"]))

        recalls.append(float(tree_height_metadata_dic[mutation_rate]["recall"]))
        precisions.append(float(tree_height_metadata_dic[mutation_rate]["precision"]))
        f1s.append(float(tree_height_metadata_dic[mutation_rate]["f1_score"]))

    result_path = root_dir / "results"

    save_path_calculate_intersection_sizes_times = result_path / "tree_height_vs_calculate_intersection_sizes_times.png"

    save_path_tps = result_path / "tree_height_vs_tps.png"
    save_path_mcs = result_path / "tree_height_vs_mcs.png"
    save_path_fps = result_path / "tree_height_vs_fps.png"
    save_path_fns = result_path / "tree_height_vs_fns.png"

    save_path_recalls = result_path / "tree_height_vs_recalls.png"
    save_path_precisions = result_path / "tree_height_vs_precisions.png"
    save_path_f1s = result_path / "tree_height_vs_f1s.png"

    viz_utils.plot_xy_data(tree_heights, calculate_intersection_sizes_times, "Tree Height vs Calculate Intersection Sizes Times", "Tree Height", "Calculate Intersections Sizes Time (s)", "lines", save_path_calculate_intersection_sizes_times)

    viz_utils.plot_xy_data(tree_heights, tps, "Tree Height vs True Positive Count", "Tree Height", "True Positive Count", "lines", save_path_tps)
    viz_utils.plot_xy_data(tree_heights, mcs, "Tree Height vs Misclassified Count", "Tree Height", "Misclassified Count", "lines", save_path_mcs)
    viz_utils.plot_xy_data(tree_heights, fps, "Tree Height vs False Positive Count", "Tree Height", "False Positive Count", "lines", save_path_fps)
    viz_utils.plot_xy_data(tree_heights, fns, "Tree Height vs False Negative Count", "Tree Height", "False Negative Count", "lines", save_path_fns)

    viz_utils.plot_xy_data(tree_heights, recalls, "Tree Height vs Recall", "Tree Height", "Recall (%)", "lines", save_path_recalls)
    viz_utils.plot_xy_data(tree_heights, precisions, "Tree Height vs Precisions", "Tree Height", "Precision (%)", "lines", save_path_precisions)
    viz_utils.plot_xy_data(tree_heights, f1s, "Tree Height vs F1 Score", "Tree Height", "F1 Score (%)", "lines", save_path_f1s)

def marginalize_tree_height_results(root_dir: Path, folders: list[str]):

    tree_heights = [[] for _ in folders]

    calculate_intersection_sizes_times = [[] for _ in folders]

    tps = [[] for _ in folders]
    mcs = [[] for _ in folders]
    fps = [[] for _ in folders]
    fns = [[] for _ in folders]

    recalls = [[] for _ in folders]
    precisions = [[] for _ in folders]
    f1s = [[] for _ in folders]

    for i in range(len(folders)):
        dir_name = folders[i]
        tree_height_metadata_dic = read_metadata_tree_height_boundary(root_dir / dir_name)

        for tree_height in sorted(tree_height_metadata_dic.keys()):
            tree_heights[i].append(tree_height)
            calculate_intersection_sizes_times[i].append(float(tree_height_metadata_dic[tree_height]["calculate_intersection_sizes_time"]))

            tps[i].append(int(tree_height_metadata_dic[tree_height]["tp"]))
            mcs[i].append(int(tree_height_metadata_dic[tree_height]["mc"]))
            fps[i].append(int(tree_height_metadata_dic[tree_height]["fp"]))
            fns[i].append(int(tree_height_metadata_dic[tree_height]["fn"]))

            recalls[i].append(float(tree_height_metadata_dic[tree_height]["recall"]))
            precisions[i].append(float(tree_height_metadata_dic[tree_height]["precision"]))
            f1s[i].append(float(tree_height_metadata_dic[tree_height]["f1_score"]))

    result_path = root_dir / "results"

    # save separate data series
    save_path_calculate_intersection_sizes_times_separate_series = result_path / "tree_height_vs_calculate_intersection_sizes_times_separate_series.png"

    save_path_tps_separate_series = result_path / "tree_height_vs_tps_separate_series.png"
    save_path_mcs_separate_series = result_path / "tree_height_vs_mcs_separate_series.png"
    save_path_fps_separate_series = result_path / "tree_height_vs_fps_separate_series.png"
    save_path_fns_separate_series = result_path / "tree_height_vs_fns_separate_series.png"

    save_path_recalls_separate_series = result_path / "tree_height_vs_recalls_separate_series.png"
    save_path_precisions_separate_series = result_path / "tree_height_vs_precisions_separate_series.png"
    save_path_f1s_separate_series = result_path / "tree_height_vs_f1s_separate_series.png"

    viz_utils.plot_multiple_xy_array(tree_heights, calculate_intersection_sizes_times, "Tree Height vs Calculate Intersection Sizes Times", "Tree Height", "Calculate Intersection Sizes Time (s)", "lines", save_path_calculate_intersection_sizes_times_separate_series)

    viz_utils.plot_multiple_xy_array(tree_heights, tps, "Tree Height vs True Positive Count", "Tree Height", "True Positive Count", "lines", save_path_tps_separate_series)
    viz_utils.plot_multiple_xy_array(tree_heights, mcs, "Tree Height vs Misclassified Count", "Tree Height", "Misclassified Count", "lines", save_path_mcs_separate_series)
    viz_utils.plot_multiple_xy_array(tree_heights, fps, "Tree Height vs False Positive Count", "Tree Height", "False Positive Count", "lines", save_path_fps_separate_series)
    viz_utils.plot_multiple_xy_array(tree_heights, fns, "Tree Height vs False Negative Count", "Tree Height", "False Negative Count", "lines", save_path_fns_separate_series)

    viz_utils.plot_multiple_xy_array(tree_heights, recalls, "Tree Height vs Recall", "Tree Height", "Recall (%)", "lines", save_path_recalls_separate_series)
    viz_utils.plot_multiple_xy_array(tree_heights, precisions, "Tree Height vs Precisions", "Tree Height", "Precision (%)", "lines", save_path_precisions_separate_series)
    viz_utils.plot_multiple_xy_array(tree_heights, f1s, "Tree Height vs F1 Score", "Tree Height", "F1 Score (%)", "lines", save_path_f1s_separate_series)

    # save marginalized data
    tree_heights_marginalized = np.mean(tree_heights, axis=0)

    calculate_intersection_sizes_times_marginalized = np.mean(calculate_intersection_sizes_times, axis=0)

    tps_marginalized = np.mean(tps, axis=0)
    mcs_marginalized = np.mean(mcs, axis=0)
    fps_marginalized = np.mean(fps, axis=0)
    fns_marginalized = np.mean(fns, axis=0)

    recalls_marginalized = np.mean(recalls, axis=0)
    precisions_marginalized = np.mean(precisions, axis=0)
    f1s_marginalized = np.mean(f1s, axis=0)


    save_path_calculate_intersection_sizes_times_marginalized = result_path / "tree_height_vs_calculate_intersection_sizes_times_marginalized.png"

    save_path_tps_marginalized = result_path / "tree_height_vs_tps_marginalized.png"
    save_path_mcs_marginalized = result_path / "tree_height_vs_mcs_marginalized.png"
    save_path_fps_marginalized = result_path / "tree_height_vs_fps_marginalized.png"
    save_path_fns_marginalized = result_path / "tree_height_vs_fns_marginalized.png"

    save_path_recalls_marginalized = result_path / "tree_height_vs_recalls_marginalized.png"
    save_path_precisions_marginalized = result_path / "tree_height_vs_precisions_marginalized.png"
    save_path_f1s_marginalized = result_path / "tree_height_vs_f1s_marginalized.png"

    viz_utils.plot_xy_data(tree_heights_marginalized, calculate_intersection_sizes_times_marginalized, "Tree Height vs Calculate Intersection Sizes Times", "Tree Height", "Calculate Intersection Sizes Time (s)", "lines", save_path_calculate_intersection_sizes_times_marginalized)

    viz_utils.plot_xy_data(tree_heights_marginalized, tps_marginalized, "Tree Height vs True Positive Count", "Tree Height", "True Positive Count", "lines", save_path_tps_marginalized)
    viz_utils.plot_xy_data(tree_heights_marginalized, mcs_marginalized, "Tree Height vs Misclassified Count", "Tree Height", "Misclassified Count", "lines", save_path_mcs_marginalized)
    viz_utils.plot_xy_data(tree_heights_marginalized, fps_marginalized, "Tree Height vs False Positive Count", "Tree Height", "False Positive Count", "lines", save_path_fps_marginalized)
    viz_utils.plot_xy_data(tree_heights_marginalized, fns_marginalized, "Tree Height vs False Negative Count", "Tree Height", "False Negative Count", "lines", save_path_fns_marginalized)

    viz_utils.plot_xy_data(tree_heights_marginalized, recalls_marginalized, "Tree Height vs Recall", "Tree Height", "Recall (%)", "lines", save_path_recalls_marginalized)
    viz_utils.plot_xy_data(tree_heights_marginalized, precisions_marginalized, "Tree Height vs Precisions", "Tree Height", "Precision (%)", "lines", save_path_precisions_marginalized)
    viz_utils.plot_xy_data(tree_heights_marginalized, f1s_marginalized, "Tree Height vs F1 Score", "Tree Height", "F1 Score (%)", "lines", save_path_f1s_marginalized)

def marginalize_mutation_rate_results(root_dir: Path, folders: list[str]):

    mutation_rates = [[] for _ in folders]

    calculate_intersection_sizes_times = [[] for _ in folders]

    tps = [[] for _ in folders]
    mcs = [[] for _ in folders]
    fps = [[] for _ in folders]
    fns = [[] for _ in folders]

    recalls = [[] for _ in folders]
    precisions = [[] for _ in folders]
    f1s = [[] for _ in folders]

    for i in range(len(folders)):
        dir_name = folders[i]
        mutation_rate_metadata_dic = read_metadata_mutation_rate_boundary(root_dir / dir_name)

        for mutation_rate in sorted(mutation_rate_metadata_dic.keys()):
            mutation_rates[i].append(mutation_rate)
            calculate_intersection_sizes_times[i].append(float(mutation_rate_metadata_dic[mutation_rate]["calculate_intersection_sizes_time"]))

            tps[i].append(int(mutation_rate_metadata_dic[mutation_rate]["tp"]))
            mcs[i].append(int(mutation_rate_metadata_dic[mutation_rate]["mc"]))
            fps[i].append(int(mutation_rate_metadata_dic[mutation_rate]["fp"]))
            fns[i].append(int(mutation_rate_metadata_dic[mutation_rate]["fn"]))

            recalls[i].append(float(mutation_rate_metadata_dic[mutation_rate]["recall"]))
            precisions[i].append(float(mutation_rate_metadata_dic[mutation_rate]["precision"]))
            f1s[i].append(float(mutation_rate_metadata_dic[mutation_rate]["f1_score"]))

    result_path = root_dir / "results"

    print(mutation_rates)
    print(calculate_intersection_sizes_times)

    # save separate data series
    save_path_calculate_intersection_sizes_times_separate_series = result_path / "mutation_rate_vs_calculate_intersection_sizes_times_separate_series.png"

    save_path_tps_separate_series = result_path / "mutation_rate_vs_tps_separate_series.png"
    save_path_mcs_separate_series = result_path / "mutation_rate_vs_mcs_separate_series.png"
    save_path_fps_separate_series = result_path / "mutation_rate_vs_fps_separate_series.png"
    save_path_fns_separate_series = result_path / "mutation_rate_vs_fns_separate_series.png"

    save_path_recalls_separate_series = result_path / "mutation_rate_vs_recalls_separate_series.png"
    save_path_precisions_separate_series = result_path / "mutation_rate_vs_precisions_separate_series.png"
    save_path_f1s_separate_series = result_path / "mutation_rate_vs_f1s_separate_series.png"

    viz_utils.plot_multiple_xy_array(mutation_rates, calculate_intersection_sizes_times,"Mutation Rate vs Calculate Intersection Sizes Times","Mutation Rate","Calculate Intersection Sizes Time (s)", "lines", save_path_calculate_intersection_sizes_times_separate_series)

    viz_utils.plot_multiple_xy_array(mutation_rates, tps, "Mutation Rate vs True Positive Count", "Mutation Rate","True Positive Count", "lines", save_path_tps_separate_series)
    viz_utils.plot_multiple_xy_array(mutation_rates, mcs, "Mutation Rate vs Misclassified Count", "Mutation Rate","Misclassified Count", "lines", save_path_mcs_separate_series)
    viz_utils.plot_multiple_xy_array(mutation_rates, fps, "Mutation Rate vs False Positive Count", "Mutation Rate","False Positive Count", "lines", save_path_fps_separate_series)
    viz_utils.plot_multiple_xy_array(mutation_rates, fns, "Mutation Rate vs False Negative Count", "Mutation Rate","False Negative Count", "lines", save_path_fns_separate_series)

    viz_utils.plot_multiple_xy_array(mutation_rates, recalls, "Mutation Rate vs Recall", "Mutation Rate", "Recall (%)", "lines",save_path_recalls_separate_series)
    viz_utils.plot_multiple_xy_array(mutation_rates, precisions, "Mutation Rate vs Precisions", "Mutation Rate", "Precision (%)","lines", save_path_precisions_separate_series)
    viz_utils.plot_multiple_xy_array(mutation_rates, f1s, "Mutation Rate vs F1 Score", "Mutation Rate", "F1 Score (%)", "lines",save_path_f1s_separate_series)

    # save marginalized data
    mutation_rates_marginalized = np.mean(mutation_rates, axis=0)

    calculate_intersection_sizes_times_marginalized = np.mean(calculate_intersection_sizes_times, axis=0)

    tps_marginalized = np.mean(tps, axis=0)
    mcs_marginalized = np.mean(mcs, axis=0)
    fps_marginalized = np.mean(fps, axis=0)
    fns_marginalized = np.mean(fns, axis=0)

    recalls_marginalized = np.mean(recalls, axis=0)
    precisions_marginalized = np.mean(precisions, axis=0)
    f1s_marginalized = np.mean(f1s, axis=0)

    save_path_calculate_intersection_sizes_times_marginalized = result_path / "mutation_rates_vs_calculate_intersection_sizes_times_marginalized.png"

    save_path_tps_marginalized = result_path / "mutation_rates_vs_tps_marginalized.png"
    save_path_mcs_marginalized = result_path / "mutation_rates_vs_mcs_marginalized.png"
    save_path_fps_marginalized = result_path / "mutation_rates_vs_fps_marginalized.png"
    save_path_fns_marginalized = result_path / "mutation_rates_vs_fns_marginalized.png"

    save_path_recalls_marginalized = result_path / "mutation_rates_vs_recalls_marginalized.png"
    save_path_precisions_marginalized = result_path / "mutation_rates_vs_precisions_marginalized.png"
    save_path_f1s_marginalized = result_path / "mutation_rates_vs_f1s_marginalized.png"

    viz_utils.plot_xy_data(mutation_rates_marginalized, calculate_intersection_sizes_times_marginalized, "Tree Height vs Calculate Intersection Sizes Times", "Mutation Rate", "Calculate Intersection Sizes Time (s)","lines", save_path_calculate_intersection_sizes_times_marginalized)

    viz_utils.plot_xy_data(mutation_rates_marginalized, tps_marginalized, "Mutation Rate vs True Positive Count", "Mutation Rate","True Positive Count", "lines", save_path_tps_marginalized)
    viz_utils.plot_xy_data(mutation_rates_marginalized, mcs_marginalized, "Mutation Rate vs Misclassified Count", "Mutation Rate","Misclassified Count", "lines", save_path_mcs_marginalized)
    viz_utils.plot_xy_data(mutation_rates_marginalized, fps_marginalized, "Mutation Rate vs False Positive Count", "Mutation Rate","False Positive Count", "lines", save_path_fps_marginalized)
    viz_utils.plot_xy_data(mutation_rates_marginalized, fns_marginalized, "Mutation Rate vs False Negative Count", "Mutation Rate","False Negative Count", "lines", save_path_fns_marginalized)

    viz_utils.plot_xy_data(mutation_rates_marginalized, recalls_marginalized, "Mutation Rate vs Recall", "Mutation Rate", "Recall (%)","lines", save_path_recalls_marginalized)
    viz_utils.plot_xy_data(mutation_rates_marginalized, precisions_marginalized, "Mutation Rate vs Precisions", "Mutation Rate","Precision (%)", "lines", save_path_precisions_marginalized)
    viz_utils.plot_xy_data(mutation_rates_marginalized, f1s_marginalized, "Mutation Rate vs F1 Score", "Mutation Rate", "F1 Score (%)","lines", save_path_f1s_marginalized)

def get_metadata_variable(root_dir: Path, variable_name: str):
    metadata_path = root_dir / "metadata.out"

    if not metadata_path.exists():
        raise FileNotFoundError(f"'metadata.out' not found in: {metadata_path}")

    with open(metadata_path, "r") as f:
        for line in f:
            key, value = line.split(": ")
            if key == variable_name:
                return value

    # Raise error if the key was not found
    raise KeyError(f"Variable '{variable_name}' not found in {metadata_path}")

def parse_metadata_independent_dependent_variable(root_dir: Path, dependent_variable_str: str, independent_variable_factor: float=1):
    dependent_variables = []
    independent_variables = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "metadata.out" in filenames:
            dependent_variable = float(get_metadata_variable(Path(dirpath), dependent_variable_str))
            dependent_variables.append(dependent_variable)

            independent_variable = utils.extract_trailing_number(Path(dirpath).parent)
            independent_variables.append(independent_variable)

    independent_variables, dependent_variables = utils.sort_lists_by_first(independent_variables, dependent_variables)
    independent_variables *= independent_variable_factor
    return independent_variables, dependent_variables

if __name__ == "__main__":
    pass