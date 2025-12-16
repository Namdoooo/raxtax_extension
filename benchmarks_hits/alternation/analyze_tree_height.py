from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations_with_list
from analysis.metadata_loader import aggregate_all_memory_iterations
from analysis.metadata_loader import aggregate_all_folders_with_list
from analysis.viz import plot_benchmark
from analysis.viz import plot_grouped_boxplots
from analysis.significance_analyzer import run_significance_analysis
from matplotlib.pyplot import ylabel
from raxtax_extension_prototype.utils import create_folder

if __name__=="__main__":
    base_dir_alternation = Path(__file__).resolve().relative_to(Path.cwd()).parent
    base_dir_alternation_t003 = base_dir_alternation.parent / "alternation_t003"
    base_dir_alternation_t017 = base_dir_alternation.parent / "alternation_t017"

    independent_var_name = "disorientation_probability"
    x_col = "Average Branch Length"

    iteration_dir_list = [base_dir_alternation / f"iteration{i}" for i in range(1, 31)]
    combined_metadata_path_alternation = aggregate_all_iterations_with_list(base_dir_alternation, independent_var_name, iteration_dir_list)
    df_alternation = pd.read_csv(combined_metadata_path_alternation)
    df_alternation[x_col] = 0.01

    folders_dir_list = [base_dir_alternation_t003 / "oriented", base_dir_alternation_t003 / "disoriented"]
    combined_metadata_path_alternation_t003 = aggregate_all_folders_with_list(base_dir_alternation_t003, independent_var_name, folders_dir_list)
    df_alternation_t003 = pd.read_csv(combined_metadata_path_alternation_t003)
    df_alternation_t003[x_col] = 0.003

    q1 = df_alternation_t003[df_alternation_t003[independent_var_name] == -1]["f1_score"].quantile(0.25)
    q2 = df_alternation_t003[df_alternation_t003[independent_var_name] == -1]["f1_score"].quantile(0.50)
    q3 = df_alternation_t003[df_alternation_t003[independent_var_name] == -1]["f1_score"].quantile(0.75)
    print("alternation_t003 oriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    q1 = df_alternation_t003[df_alternation_t003[independent_var_name] == 0.5]["f1_score"].quantile(0.25)
    q2 = df_alternation_t003[df_alternation_t003[independent_var_name] == 0.5]["f1_score"].quantile(0.50)
    q3 = df_alternation_t003[df_alternation_t003[independent_var_name] == 0.5]["f1_score"].quantile(0.75)
    print("alternation_t003 disoriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    df_pivot = df_alternation_t003.pivot(index="iteration", columns=independent_var_name, values="f1_score")
    df_pivot["difference"] = df_pivot[-1] - df_pivot[0.5]
    print(df_pivot["difference"].agg(["mean"]))
    print(df_pivot)




    folders_dir_list = [base_dir_alternation_t017 / "oriented", base_dir_alternation_t017 / "disoriented"]
    combined_metadata_path_alternation_t017 = aggregate_all_folders_with_list(base_dir_alternation_t017, independent_var_name, folders_dir_list)
    df_alternation_t017 = pd.read_csv(combined_metadata_path_alternation_t017)
    df_alternation_t017[x_col] = 0.017

    q1 = df_alternation_t017[df_alternation_t017[independent_var_name] == -1]["f1_score"].quantile(0.25)
    q2 = df_alternation_t017[df_alternation_t017[independent_var_name] == -1]["f1_score"].quantile(0.50)
    q3 = df_alternation_t017[df_alternation_t017[independent_var_name] == -1]["f1_score"].quantile(0.75)
    print("df_alternation_t017 oriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    q1 = df_alternation_t017[df_alternation_t017[independent_var_name] == 0.5]["f1_score"].quantile(0.25)
    q2 = df_alternation_t017[df_alternation_t017[independent_var_name] == 0.5]["f1_score"].quantile(0.50)
    q3 = df_alternation_t017[df_alternation_t017[independent_var_name] == 0.5]["f1_score"].quantile(0.75)
    print("df_alternation_t017 disoriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    df_pivot = df_alternation_t017.pivot(index="iteration", columns=independent_var_name, values="f1_score")
    df_pivot["difference"] = df_pivot[-1] - df_pivot[0.5]
    print(df_pivot["difference"].agg(["mean"]))
    print(df_pivot)

    combined_df = pd.concat([df_alternation, df_alternation_t003, df_alternation_t017], ignore_index=True)
    combined_df[independent_var_name] = combined_df[independent_var_name].apply(lambda x: "Oriented Queries" if x == -1 else "Disoriented Queries")
    df_selected = combined_df[["iteration", independent_var_name, "f1_score", x_col]]
    print(df_selected)

    output_path = base_dir_alternation / "alternation_tree_height_box_plot.pdf"
    condition_col = "method"

    plot_grouped_boxplots(df=df_selected, x_col=x_col, y_col="f1_score", hue_col=independent_var_name, ylabel="F1 Score", xlabel=x_col, save_path=output_path)

"""

alternation_t003 oriented:
q1: 0.6924999999999999
q2: 0.72
q3: 0.74
alternation_t003 disoriented:
q1: 0.6924999999999999
q2: 0.72
q3: 0.74

df_alternation_t017 oriented:
q1: 0.97
q2: 0.975
q3: 0.98
df_alternation_t017 disoriented:
q1: 0.96
q2: 0.97
q3: 0.9775
mean    0.006333
"""