from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations_with_list
from analysis.metadata_loader import aggregate_all_memory_iterations
from analysis.viz import plot_benchmark
from analysis.significance_analyzer import run_significance_analysis
from raxtax_extension_prototype.utils import create_folder

from analysis.metadata_loader import aggregate_folder
from analysis.metadata_loader import aggregate_all_folders_with_list

if __name__=="__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    output_path = base_dir / "significance_test.tsv"

    independent_var_name = "disorientation_probability"

    hue_col_name = "name"
    hue_name = "raxtax+"

    folders_dir_list = [base_dir / "oriented", base_dir / "disoriented"]
    combined_metadata_path = aggregate_all_folders_with_list(base_dir, independent_var_name, folders_dir_list)

    df_all = pd.read_csv(combined_metadata_path)
    print(df_all["total_execution_time"].mean())

    df_selected = df_all[["iteration", independent_var_name, "f1_score"]]

    run_significance_analysis(df_selected, "iteration", "f1_score", independent_var_name, (-1, 0.5), output_path,
                              "greater")
