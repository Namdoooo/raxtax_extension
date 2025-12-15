from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations
from analysis.metadata_loader import aggregate_all_memory_iterations
from analysis.viz import plot_benchmark
from raxtax_extension_prototype.utils import create_folder

if __name__=="__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    independent_var_name = "sequence_length"
    xlabel = "Sequence Length"

    hue_col_name = "name"
    hue_name = "raxtax+"

    #analyze memory usage
    dependent_var_name = "execute_raxtax peak (GB)"
    ylabel = "Memory (GB)"

    plot_path = base_dir / f"{independent_var_name}_vs_memory.pdf"


    combined_memory_data_path = aggregate_all_memory_iterations(base_dir, independent_var_name)
    df_all = pd.read_csv(combined_memory_data_path)
    df_all[dependent_var_name] = df_all[dependent_var_name]
    df_all[hue_col_name] = hue_name
    df_selected = df_all[[independent_var_name, dependent_var_name, hue_col_name]]
    print(df_selected)

    plot_benchmark(df_selected, independent_var_name, dependent_var_name, hue_col_name, xlabel, ylabel,
                   xgrid_exact=True, error="sd", save_path=plot_path)

    dependent_var_names = ["generate_dataset peak (GB)", "generate_dataset parent_peak (GB)", "generate_dataset children_peak (GB)",
                           "calculate_lookup peak (GB)", "calculate_lookup parent_peak (GB)", "calculate_lookup children_peak (GB)",
                           "execute_raxtax peak (GB)", "execute_raxtax parent_peak (GB)", "execute_raxtax children_peak (GB)"]

    plot_dir = base_dir / "plots"
    create_folder(plot_dir)

    for dependent_var_name in dependent_var_names:
        plot_name = f"{independent_var_name}_vs_{dependent_var_name}.pdf"
        ylabel = dependent_var_name

        plot_path = plot_dir / plot_name

        df_selected = df_all[[independent_var_name, dependent_var_name, hue_col_name]]

        plot_benchmark(df_selected, independent_var_name, dependent_var_name, hue_col_name, xlabel, ylabel,
                       xgrid_exact=True, error="sd", save_path=plot_path)



