from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations_with_list
from analysis.metadata_loader import aggregate_all_memory_iterations
from analysis.viz import plot_benchmark
from analysis.viz import plot_paired_boxplot
from analysis.significance_analyzer import run_significance_analysis
from raxtax_extension_prototype.utils import create_folder

if __name__=="__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    output_path = base_dir / "significance_test.tsv"

    independent_var_name = "disorientation_probability"

    hue_col_name = "name"
    hue_name = "raxtax+"

    iteration_dir_list = [base_dir / f"iteration{i}" for i in range(1, 31)]

    combined_metadata_path = aggregate_all_iterations_with_list(base_dir, independent_var_name, iteration_dir_list)
    df_all = pd.read_csv(combined_metadata_path)



    df_selected = df_all[["iteration", independent_var_name, "f1_score"]]

    print("oriented queries: data values")
    q1_oriented = df_selected[df_selected[independent_var_name] == -1]["f1_score"].quantile(0.25)
    q2_oriented = df_selected[df_selected[independent_var_name] == -1]["f1_score"].quantile(0.5)
    q3_oriented = df_selected[df_selected[independent_var_name] == -1]["f1_score"].quantile(0.75)
    print(f"q1: {q1_oriented}")
    print(f"q2: {q2_oriented}")
    print(f"q3: {q3_oriented}")


    print("disoriented queries: data values")
    q1_disoriented = df_selected[df_selected[independent_var_name] == 0.5]["f1_score"].quantile(0.25)
    q2_disoriented = df_selected[df_selected[independent_var_name] == 0.5]["f1_score"].quantile(0.5)
    q3_disoriented = df_selected[df_selected[independent_var_name] == 0.5]["f1_score"].quantile(0.75)
    print(f"q1: {q1_disoriented}")
    print(f"q2: {q2_disoriented}")
    print(f"q3: {q3_disoriented}")

    df_pivot = df_all.pivot(index="iteration", columns=independent_var_name, values="f1_score")
    df_pivot["difference"] = df_pivot[-1] - df_pivot[0.5]
    print(df_pivot["difference"].agg(["mean"]))
    print(df_pivot)

    run_significance_analysis(df_selected, "iteration", "f1_score", independent_var_name, (-1, 0.5), output_path, "greater")

    output_path = base_dir / "alternation_box_plot.pdf"

    condition_col = "method"
    df_all[condition_col] = df_all[independent_var_name].apply(lambda x: "Oriented Queries" if x == -1 else "Disoriented Queries")
    df_selected = df_all[["iteration", condition_col, "f1_score"]]

    plot_paired_boxplot(df_selected, value_col="f1_score", condition_col=condition_col, save_path=output_path, ylabel="F1 Score")

"""
oriented queries: data values
q1: 0.93
q2: 0.94
q3: 0.94
disoriented queries: data values
q1: 0.9225000000000001
q2: 0.94
q3: 0.94
mean    0.002333
"""