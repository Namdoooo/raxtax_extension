from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations
from analysis.viz import plot_benchmark
from raxtax_extension_prototype.utils import create_folder

if __name__=="__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    independent_var_name = "tree_height"
    xlabel = "Tree Height"
    dependent_var_name = "f1_score"
    ylabel = "F1 Score"
    hue_col_name = "name"
    hue_name = "raxtax+"

    plot_name = "tree_height_vs_f1_score.png"
    plot_path = base_dir / plot_name

    combined_metadata_path = aggregate_all_iterations(base_dir, independent_var_name)
    df_all = pd.read_csv(combined_metadata_path)

    df_selected = df_all[[independent_var_name, dependent_var_name]]
    df_selected[hue_col_name] = hue_name

    plot_benchmark(df_selected, independent_var_name, dependent_var_name, hue_col_name, xlabel, ylabel,
                   xgrid_exact=True, error="sd", save_path=plot_path)


    dependent_var_names = ["reference_count", "query_count", "total_execution_time", "reference_parse_time",
                           "query_parse_time", "orient_queries_time", "calculate_intersection_sizes_time",
                           "average_reference_processing_time", "average_prob_calculation_time", "tp", "mc", "fp", "fn",
                           "recall", "precision", "f1_score"]
    xlabel = independent_var_name.replace("_", " ")
    ylabel_list = [s.replace("_", " ") for s in dependent_var_names]

    plot_names = []
    for dependent_var_name in dependent_var_names:
        plot_name = f"{independent_var_name}_vs_{dependent_var_name}.png"
        plot_names.append(plot_name)


    plot_dir = base_dir / "plots"
    create_folder(plot_dir)

    for i in range(len(dependent_var_names)):
        dependent_var_name = dependent_var_names[i]
        ylabel = ylabel_list[i]
        plot_name = plot_names[i]

        plot_path = plot_dir / plot_name

        df_selected = df_all[[independent_var_name, dependent_var_name]]

        hue_col_name = "name"
        df_selected[hue_col_name] = "raxtax+"

        plot_benchmark(df_selected, independent_var_name, dependent_var_name, hue_col_name, xlabel, ylabel,
                       xgrid_exact=True, error="sd", save_path=plot_path)
