from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations
from analysis.viz import plot_benchmark
from analysis.viz import plot_paired_lines
from analysis.significance_analyzer import run_significance_analysis
from numpy.lib.function_base import interp
from raxtax_extension_prototype.utils import create_folder

if __name__=="__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    independent_var_name = "tree_height"
    xlabel = "Average Branch Length"
    dependent_var_name = "f1_score"
    ylabel = "F1 Score"
    hue_col_name = "name"
    hue_name = "raxtax+"

    plot_name = "tree_height_vs_f1_score.pdf"
    plot_path = base_dir / plot_name

    combined_metadata_path = aggregate_all_iterations(base_dir, independent_var_name)
    df_all = pd.read_csv(combined_metadata_path)
    df_all[independent_var_name] = df_all[independent_var_name] * 0.1
    df_all[hue_col_name] = hue_name

    df_selected = df_all[[independent_var_name, dependent_var_name, hue_col_name]]

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
        plot_name = f"{independent_var_name}_vs_{dependent_var_name}.pdf"
        plot_names.append(plot_name)


    plot_dir = base_dir / "plots"
    create_folder(plot_dir)

    for i in range(len(dependent_var_names)):
        dependent_var_name = dependent_var_names[i]
        ylabel = ylabel_list[i]
        plot_name = plot_names[i]

        plot_path = plot_dir / plot_name

        df_selected = df_all[[independent_var_name, dependent_var_name, hue_col_name]]

        plot_benchmark(df_selected, independent_var_name, dependent_var_name, hue_col_name, xlabel, ylabel,
                       xgrid_exact=True, error="sd", save_path=plot_path)

    #create paired line plot
    df_all_tree_height_complement = pd.read_csv(combined_metadata_path)
    tree_height_benchmark_metadata_path = base_dir.parent / "tree_height_benchmark" / "combined_metadata.csv"
    print(combined_metadata_path)
    print(tree_height_benchmark_metadata_path)
    df_all_tree_height_benchmark = pd.read_csv(tree_height_benchmark_metadata_path)

    iteration_name = "iteration"
    cond_var_name = "method"
    ylabel = "F1 Score"
    group_names = ["oriented queries", "disoriented queries"]
    df_tree_height_benchmark = df_all_tree_height_benchmark[[independent_var_name, dependent_var_name]]
    df_tree_height_complement = df_all_tree_height_complement[[independent_var_name, dependent_var_name]]

    df_mean_tree_height_benchmark = df_tree_height_benchmark.groupby(independent_var_name).mean()
    df_mean_tree_height_benchmark = df_mean_tree_height_benchmark.copy()
    df_mean_tree_height_benchmark[cond_var_name] = group_names[0]

    df_mean_tree_height_complement = df_tree_height_complement.groupby(independent_var_name).mean()
    df_mean_tree_height_complement = df_mean_tree_height_complement.copy()
    df_mean_tree_height_complement[cond_var_name] = group_names[1]

    df_combined = pd.concat([df_mean_tree_height_benchmark, df_mean_tree_height_complement])

    paired_line_plot_path = base_dir / "paired_line_tree_height_f1_plot.pdf"
    plot_paired_lines(df=df_combined, id_col=independent_var_name, value_col=dependent_var_name, condition_col=cond_var_name, ylabel=ylabel, save_path=paired_line_plot_path)

    #execute significance analysis
    significance_result_path = base_dir / "significance_test.tsv"
    run_significance_analysis(df=df_combined, id_col=independent_var_name, value_col=dependent_var_name, condition_col=cond_var_name,
                              group_names=group_names, output_path=significance_result_path, alternative="greater")

