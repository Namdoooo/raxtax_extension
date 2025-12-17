"""
metadata_loader.py

Purpose
-------
Provides functions for aggregating evaluation results.
"""

from pathlib import Path
import pandas as pd
import yaml

def parse_metadata_file(file_path):
    """
    Parses a file containing key–value pairs and returns
    the extracted information as a dictionary.
    """
    data = {}
    with open(file_path, "r") as f:
        for line in f:
            if ':' in line:
                key, value = line.strip().split(":", 1)
                data[key.strip()] = value.strip()
    return data

def aggregate_iteration(iteration_path: Path, independent_var_name: str):
    """
    Aggregates evaluation results of all experiments within
    an iteration into a CSV file.
    """
    exp_dir_list = sorted([p for p in iteration_path.iterdir() if p.is_dir() and p.name != "__pycache__" and p.name != "references"])
    rows = []

    for exp_dir in exp_dir_list:
        config_path = list(exp_dir.glob("config.yaml"))[0]
        metadata_path = list(exp_dir.glob("*/metadata.out"))[0]

        with config_path.open("r") as f:
            config = yaml.safe_load(f)
        metadata = parse_metadata_file(metadata_path)

        dependent_var = config[independent_var_name]

        metadata[independent_var_name] = dependent_var
        rows.append(metadata)

    df = pd.DataFrame(rows)

    aggregated_metadata_path = iteration_path / "aggregated_metadata.csv"

    if not df.empty:
        cols = [independent_var_name] + [col for col in df.columns if col not in independent_var_name]
        df = df[cols]
        df = df.sort_values(by=independent_var_name)
        df.to_csv(aggregated_metadata_path, index=False)
        print(f"Saved: {aggregated_metadata_path}")
    else:
        raise ValueError(f"No metadata found in {iteration_path}")

    return aggregated_metadata_path

def aggregate_all_iterations(base_dir: Path, independent_var_name: str):
    """
    Aggregates evaluation results from all iterations into a CSV file.
    """
    iteration_col_name = "iteration"

    iteration_dir_list = sorted([p for p in base_dir.iterdir() if p.is_dir() and p.name.startswith("iteration")])
    dfs = []

    for iteration_dir in iteration_dir_list:
        print(f"Processing: {iteration_dir}")

        aggregated_metadata_path = aggregate_iteration(iteration_dir, independent_var_name=independent_var_name)
        df = pd.read_csv(aggregated_metadata_path)
        df[iteration_col_name] = iteration_dir.name.strip(iteration_col_name)
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    target_cols = ["iteration", independent_var_name]
    cols = target_cols + [col for col in df_all.columns if col not in target_cols]
    df_all = df_all[cols]
    df_all = df_all.sort_values(by=[iteration_col_name, independent_var_name])

    combined_metadata_path = base_dir / "combined_metadata.csv"
    df_all.to_csv(combined_metadata_path, index=False)
    print(f"Saved: {combined_metadata_path}")

    return combined_metadata_path

def aggregate_all_iterations_with_list(base_dir: Path, independent_var_name: str, iteration_dir_list: list):
    """
    Aggregates evaluation results from all iterations listed in
    iteration_dir_list into a CSV file.
    """
    iteration_col_name = "iteration"

    dfs = []

    for iteration_dir in iteration_dir_list:
        print(f"Processing: {iteration_dir}")

        aggregated_metadata_path = aggregate_iteration(iteration_dir, independent_var_name=independent_var_name)
        df = pd.read_csv(aggregated_metadata_path)
        df[iteration_col_name] = iteration_dir.name.strip(iteration_col_name)
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    target_cols = ["iteration", independent_var_name]
    cols = target_cols + [col for col in df_all.columns if col not in target_cols]
    df_all = df_all[cols]
    df_all = df_all.sort_values(by=[iteration_col_name, independent_var_name])

    combined_metadata_path = base_dir / "combined_metadata.csv"
    df_all.to_csv(combined_metadata_path, index=False)
    print(f"Saved: {combined_metadata_path}")

    return combined_metadata_path

def aggregate_folder(base_dir: Path, independent_var_name: str):
    """
    Aggregates evaluation results within a directory where experiments
    differ only in their iteration index and stores them in a CSV file.
    """
    exp_dir_list = sorted([p for p in base_dir.iterdir() if p.is_dir() and p.name != "__pycache__"])
    rows = []
    iteration_col_name = "iteration"

    for exp_dir in exp_dir_list:
        config_path = list(exp_dir.glob("config.yaml"))[0]
        metadata_path = list(exp_dir.glob("*/metadata.out"))[0]

        print(exp_dir.name)

        with config_path.open("r") as f:
            config = yaml.safe_load(f)
        metadata = parse_metadata_file(metadata_path)

        dependent_var = config[independent_var_name]

        metadata[independent_var_name] = dependent_var
        metadata[iteration_col_name] = exp_dir.name.strip(iteration_col_name)
        rows.append(metadata)
        print(metadata)

    df = pd.DataFrame(rows)

    aggregated_metadata_path = base_dir / "aggregated_metadata.csv"

    if not df.empty:
        cols = [independent_var_name] + [col for col in df.columns if col not in independent_var_name]
        df = df[cols]
        df = df.sort_values(by=independent_var_name)
        df.to_csv(aggregated_metadata_path, index=False)
        print(f"Saved: {aggregated_metadata_path}")
    else:
        raise ValueError(f"No metadata found in {base_dir}")

    return aggregated_metadata_path

def aggregate_all_folders_with_list(base_dir: Path, independent_var_name: str, folder_dir_list: list):
    """
    Aggregates evaluation results from multiple experiment
    partitions listed in folder_dir_list into a CSV file.

    This function is specifically designed for the alternation_m004, alternation_m008, alternation_t003 and
    alternation_t017 benchmarks, which use a different directory structure.
    """
    iteration_col_name = "iteration"
    df_all = []

    for folder_dir in folder_dir_list:
        print(f"Processing: {folder_dir}")

        aggregated_metadata_path = aggregate_folder(folder_dir, independent_var_name=independent_var_name)
        df = pd.read_csv(aggregated_metadata_path)
        df_all.append(df)

    df_all = pd.concat(df_all, ignore_index=True)
    target_cols = [iteration_col_name, independent_var_name]
    cols = target_cols + [col for col in df_all.columns if col not in target_cols]
    df_all = df_all[cols]
    df_all = df_all.sort_values(by=[iteration_col_name, independent_var_name])

    combined_metadata_path = base_dir / "combined_metadata.csv"
    df_all.to_csv(combined_metadata_path, index=False)
    print(f"Saved: {combined_metadata_path}")

    return combined_metadata_path

def aggregate_memory_iteration(iteration_path: Path, independent_var_name: str):
    """
    Aggregates memory usage measurements of all
    experiments within an iteration into a CSV file.
    """
    exp_dir_list = sorted([p for p in iteration_path.iterdir() if p.is_dir() and p.name != "__pycache__"])
    rows = []

    for exp_dir in exp_dir_list:
        config_path = list(exp_dir.glob("config.yaml"))[0]
        #memory_data_path = list(exp_dir.glob("time.log"))[0]
        memory_data_path = list(exp_dir.glob("psutil_memory_results.csv"))[0]

        with config_path.open("r") as f:
            config = yaml.safe_load(f)
        memory_data = parse_metadata_file(memory_data_path)

        dependent_var = config[independent_var_name]

        memory_data[independent_var_name] = dependent_var
        rows.append(memory_data)

    df = pd.DataFrame(rows)

    aggregated_memory_data_path = iteration_path / "aggregated_memory_data.csv"

    if not df.empty:
        cols = [independent_var_name] + [col for col in df.columns if col not in independent_var_name]
        df = df[cols]
        df = df.sort_values(by=independent_var_name)
        df.to_csv(aggregated_memory_data_path, index=False)
        print(f"Saved: {aggregated_memory_data_path}")
    else:
        raise ValueError(f"No metadata found in {iteration_path}")

    return aggregated_memory_data_path

def aggregate_all_memory_iterations(base_dir: Path, independent_var_name: str):
    """
    Aggregates memory usage measurements from all iterations into a CSV file.
    """
    iteration_col_name = "iteration"

    iteration_dir_list = sorted([p for p in base_dir.iterdir() if p.is_dir() and p.name.startswith("iteration")])
    dfs = []

    for iteration_dir in iteration_dir_list:
        print(f"Processing: {iteration_dir}")

        aggregated_memory_data_path = aggregate_memory_iteration(iteration_dir, independent_var_name=independent_var_name)
        df = pd.read_csv(aggregated_memory_data_path)
        df[iteration_col_name] = iteration_dir.name.strip(iteration_col_name)
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    target_cols = ["iteration", independent_var_name]
    cols = target_cols + [col for col in df_all.columns if col not in target_cols]
    df_all = df_all[cols]
    df_all = df_all.sort_values(by=[iteration_col_name, independent_var_name])

    combined_memory_data_path = base_dir / "combined_memory_data.csv"
    df_all.to_csv(combined_memory_data_path, index=False)
    print(f"Saved: {combined_memory_data_path}")

    return combined_memory_data_path
