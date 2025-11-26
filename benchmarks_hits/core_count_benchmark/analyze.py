from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations
from analysis.viz import plot_benchmark
from raxtax_extension_prototype.utils import create_folder

if __name__=="__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    independent_var_name = "core_count"
    dependent_var_name = "calculate_intersection_sizes_time"
    hue_col_name = "name"
    hue_name = "raxtax+"

    plot_name = "threads_vs_rel_speedup.pdf"
    plot_path = base_dir / plot_name

    combined_metadata_path = aggregate_all_iterations(base_dir, independent_var_name)

    df_all = pd.read_csv(combined_metadata_path)
    df = df_all[["iteration", independent_var_name, dependent_var_name]]
    df = df[df["core_count"] != 0]

    baseline = (
        df[df[independent_var_name] == 1]
        .loc[:, ["iteration", dependent_var_name]]
        .rename(columns={dependent_var_name: "baseline_time"})
    )

    df = df.merge(baseline, on="iteration")

    df["speed_up"] = df["baseline_time"] / df[dependent_var_name]
    df = df[[independent_var_name, "speed_up"]]
    df[hue_col_name] = hue_name

    plot_benchmark(df, "core_count", "speed_up", "name", "Threads", "rel. Speedup",
                   xgrid_exact=True, error="sd", save_path=plot_path, ref_slope=1, ref_intercept=0, ref_label="ideal")

    df_mean = df.groupby(independent_var_name)["speed_up"].agg("mean").reset_index()
    df_std = df.groupby(independent_var_name)["speed_up"].agg("std").reset_index()
    print("Mean")
    print(df_mean)
    print("Standard Deviation")
    print(df_std)



    independent_var_name = "core_count"
    dependent_var_names = ["reference_count", "query_count", "total_execution_time", "reference_parse_time",
                           "query_parse_time", "calculate_intersection_sizes_time",
                           "average_reference_processing_time", "average_prob_calculation_time", "tp", "mc", "fp", "fn",
                           "recall", "precision", "f1_score"]

    xlabel = independent_var_name.replace("_", " ")
    ylabel_list = [s.replace("_", " ") for s in dependent_var_names]

    plot_names = []
    for dependent_var_name in dependent_var_names:
        plot_name = f"{independent_var_name}_vs_{dependent_var_name}.pdf"
        plot_names.append(plot_name)

    plot_dir = base_dir / "plots"
    create_folder(plot_dir)

    for i in range(len(dependent_var_names)):
        dependent_var_name = dependent_var_names[i]
        ylabel = ylabel_list[i]
        plot_name = plot_names[i]

        plot_path = plot_dir / plot_name

        df_selected = df_all[[independent_var_name, dependent_var_name]]

        df_selected[hue_col_name] = hue_name

        plot_benchmark(df_selected, independent_var_name, dependent_var_name, hue_col_name, xlabel, ylabel,
                       xgrid_exact=True, error="sd", save_path=plot_path)