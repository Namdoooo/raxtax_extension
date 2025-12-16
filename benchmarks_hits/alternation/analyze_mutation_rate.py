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
    base_dir_alternation_m004 = base_dir_alternation.parent / "alternation_m004"
    base_dir_alternation_m008 = base_dir_alternation.parent / "alternation_m008"

    independent_var_name = "disorientation_probability"
    x_col = "Substitution Rate"

    iteration_dir_list = [base_dir_alternation / f"iteration{i}" for i in range(1, 31)]
    combined_metadata_path_alternation = aggregate_all_iterations_with_list(base_dir_alternation, independent_var_name, iteration_dir_list)
    df_alternation = pd.read_csv(combined_metadata_path_alternation)
    df_alternation[x_col] = 0

    folders_dir_list = [base_dir_alternation_m004 / "oriented", base_dir_alternation_m004 / "disoriented"]
    combined_metadata_path_alternation_m004 = aggregate_all_folders_with_list(base_dir_alternation_m004, independent_var_name, folders_dir_list)
    df_alternation_m004 = pd.read_csv(combined_metadata_path_alternation_m004)
    df_alternation_m004[x_col] = 0.04

    q1 = df_alternation_m004[df_alternation_m004[independent_var_name] == -1]["f1_score"].quantile(0.25)
    q2 = df_alternation_m004[df_alternation_m004[independent_var_name] == -1]["f1_score"].quantile(0.50)
    q3 = df_alternation_m004[df_alternation_m004[independent_var_name] == -1]["f1_score"].quantile(0.75)
    print("alternation_m004 oriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    q1 = df_alternation_m004[df_alternation_m004[independent_var_name] == 0.5]["f1_score"].quantile(0.25)
    q2 = df_alternation_m004[df_alternation_m004[independent_var_name] == 0.5]["f1_score"].quantile(0.50)
    q3 = df_alternation_m004[df_alternation_m004[independent_var_name] == 0.5]["f1_score"].quantile(0.75)
    print("alternation_m004 disoriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    df_pivot = df_alternation_m004.pivot(index="iteration", columns=independent_var_name, values="f1_score")
    df_pivot["difference"] = df_pivot[-1] - df_pivot[0.5]
    print(df_pivot["difference"].agg(["mean"]))
    print(df_pivot)




    folders_dir_list = [base_dir_alternation_m008 / "oriented", base_dir_alternation_m008 / "disoriented"]
    combined_metadata_path_alternation_m008 = aggregate_all_folders_with_list(base_dir_alternation_m008, independent_var_name, folders_dir_list)
    df_alternation_m008 = pd.read_csv(combined_metadata_path_alternation_m008)
    df_alternation_m008[x_col] = 0.08

    q1 = df_alternation_m008[df_alternation_m008[independent_var_name] == -1]["f1_score"].quantile(0.25)
    q2 = df_alternation_m008[df_alternation_m008[independent_var_name] == -1]["f1_score"].quantile(0.50)
    q3 = df_alternation_m008[df_alternation_m008[independent_var_name] == -1]["f1_score"].quantile(0.75)
    print("df_alternation_m008 oriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    q1 = df_alternation_m008[df_alternation_m008[independent_var_name] == 0.5]["f1_score"].quantile(0.25)
    q2 = df_alternation_m008[df_alternation_m008[independent_var_name] == 0.5]["f1_score"].quantile(0.50)
    q3 = df_alternation_m008[df_alternation_m008[independent_var_name] == 0.5]["f1_score"].quantile(0.75)
    print("df_alternation_m008 disoriented:")
    print(f"q1: {q1}")
    print(f"q2: {q2}")
    print(f"q3: {q3}")

    df_pivot = df_alternation_m008.pivot(index="iteration", columns=independent_var_name, values="f1_score")
    df_pivot["difference"] = df_pivot[-1] - df_pivot[0.5]
    print(df_pivot["difference"].agg(["mean"]))
    print(df_pivot)

    combined_df = pd.concat([df_alternation, df_alternation_m004, df_alternation_m008], ignore_index=True)
    combined_df[independent_var_name] = combined_df[independent_var_name].apply(lambda x: "Oriented Queries" if x == -1 else "Disoriented Queries")
    df_selected = combined_df[["iteration", independent_var_name, "f1_score", x_col]]
    print(df_selected)

    output_path = base_dir_alternation / "alternation_mutation_rate_box_plot.pdf"
    condition_col = "method"

    plot_grouped_boxplots(df=df_selected, x_col=x_col, y_col="f1_score", hue_col=independent_var_name, ylabel="F1 Score", xlabel=x_col, save_path=output_path)

"""

alternation_m004 oriented:
q1: 0.84
q2: 0.86
q3: 0.87
alternation_m004 disoriented:
q1: 0.8325
q2: 0.855
q3: 0.87
mean    0.003667

df_alternation_m008 oriented:
q1: 0.7
q2: 0.71
q3: 0.73
df_alternation_m008 disoriented:
q1: 0.69
q2: 0.71
q3: 0.73
mean    0.004
"""