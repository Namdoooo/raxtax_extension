from pathlib import Path
import pandas as pd
import yaml

def parse_metadata_file(file_path):
    data = {}
    with open(file_path, "r") as f:
        for line in f:
            if ':' in line:
                key, value = line.strip().split(":", 1)
                data[key.strip()] = value.strip()
    return data


def aggregate_iteration(iteration_path: Path, independent_var_name: str):

    exp_dir_list = sorted([p for p in iteration_path.iterdir() if p.is_dir() and p.name != "__pycache__"])
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

if __name__ == "__main__":
    metdata_path = Path("../benchmarks_hits/core_count_benchmark/iteration1/core0/results_references_queries_200/metadata.out")
    iteration_path = metdata_path.parent.parent.parent
    base_dir = iteration_path.parent

    aggregate_all_iterations(base_dir, "core_count")

