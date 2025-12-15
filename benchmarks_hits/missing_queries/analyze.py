from pathlib import Path
import pandas as pd

from analysis.metadata_loader import aggregate_all_iterations
from analysis.metadata_loader import aggregate_all_memory_iterations
from analysis.viz import plot_benchmark
from raxtax_extension_prototype.utils import create_folder

if __name__=="__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    independent_var_name = "tree_height"
    combined_metadata_path = aggregate_all_iterations(base_dir, independent_var_name)
    df_all = pd.read_csv(combined_metadata_path)
    df_all["fp_percent"] = df_all["fp"] / 200

    df_selected = df_all[["iteration", "fp_percent"]]
    print(df_selected)

    summary = (
        df_selected.groupby("iteration")["fp_percent"]
        .agg(["mean", "std"])
        .assign(fraction=lambda x: x["std"] / x["mean"])
    )

    print(summary.round(2))

"""
RESULTS
            mean   std  fraction
iteration                       
1          144.4  6.90      0.05
2          148.0  8.86      0.06
3          141.1  4.91      0.03
4          143.7  7.32      0.05
5          147.1  7.31      0.05
"""

"""
RESULTS
  fp percent mean   std  fraction
iteration                       
1          72.20  3.45      0.05
2          74.00  4.43      0.06
3          70.55  2.45      0.03
4          71.85  3.66      0.05
5          73.55  3.65      0.05
"""
"""
           mean   std  fraction
iteration                      
1          0.72  0.03      0.05
2          0.74  0.04      0.06
3          0.71  0.02      0.03
4          0.72  0.04      0.05
5          0.74  0.04      0.05
"""
