import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

def plot_benchmark(
    df,
    x_col: str,
    y_col: str,
    hue_col: str | None = None,
    xlabel: str = "X-axis",
    ylabel: str = "Y-axis",
    title: str = None,
    error: str = "sd",   # "sd", "ci", or None
    error_color: str = "#5573AA",
    ref_slope: float | None = None,
    ref_intercept: float = 0,
    ref_label: str = "ideal",
    ref_color: str = "#58BBCC",
    rotation: int | float = 0,
    xgrid_exact: bool = False,
    palette: str | list | dict | None = ["#ED6D52", "#58BBCC"],
    save_path: str | Path = None
):
    """
    Create a benchmark line plot with optional error bands and a linear reference line.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data in tidy (long) format.
    x_col, y_col, hue_col : str
        Columns for x-axis, y-axis, and grouping (legend).
    xlabel, ylabel : str
        Axis labels.
    title : str, optional
        Plot title.
    error : {"sd", "ci", None}, default=None
        Error shading option.
    ref_slope : float, optional
        Slope of optional reference line (y = slope * x + intercept).
    ref_intercept : float, default=0
        Intercept of reference line.
    ref_label : str, default="ideal"
        Label for reference line in legend.
    ref_color : str, default="teal"
        Color of the reference line (e.g. "teal", "red", "#1f77b4").
    rotation : int or float, default=0
        Rotation angle of x-axis tick labels.
    palette : str, list, dict, or None
        Seaborn color palette for data lines. Default: seaborn's deep palette.
    save_path : str or Path, optional
        If given, saves plot to this path; otherwise displays it.
    """

    sns.set_style("whitegrid")
    plt.figure(figsize=(8, 5))

    if hue_col is None:
        line_color = "#ED6D52"
        ax = sns.lineplot(
            data=df,
            x=x_col,
            y=y_col,
            color=line_color,
            marker="o",
            linewidth=2,
            errorbar=error,
            err_kws={"edgecolor": None, "alpha": 0.2, "facecolor": error_color},
        )
    else:
        ax = sns.lineplot(
            data=df,
            x=x_col,
            y=y_col,
            hue=hue_col,
            marker="o",
            linewidth=2,
            errorbar=error,
            err_kws={"edgecolor": None, "alpha": 0.2, "facecolor": error_color},
            palette=palette
        )

    if xgrid_exact:
        ax.set_xticks(sorted(df[x_col].unique()))  # tick/grid at each data x
        ax.grid(True, axis="x")

    #ax.set_xscale("log", base=2)

    # Add reference line if requested
    if ref_slope is not None:
        import numpy as np
        x_vals = np.linspace(df[x_col].min(), df[x_col].max(), 200)
        y_vals = ref_slope * x_vals + ref_intercept  # slope=1, intercept=0
        plt.plot(x_vals, y_vals, "--", color=ref_color, label=ref_label, linewidth=2)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title:
        plt.title(title)

    plt.ticklabel_format(style="plain", axis="x")  # x-axis plain numbers
    plt.ticklabel_format(style="plain", axis="y")  # y-axis plain numbers
    plt.xticks(rotation=rotation)

    ncol = df[x_col].unique().shape[0]
    if ref_slope is not None:
        ncol += 1

    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.1),
        ncol=ncol,
        frameon=False,
        title=None
    )

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Saved plot to {save_path}")
    else:
        plt.show()

if __name__ == "__main__":
    rng = np.random.default_rng(42)

    threads = [1, 2, 4, 8, 16]
    methods = ["raxtax", "sintax"]

    rows = []
    for method in methods:
        for t in threads:
            # simulate 5 runs per (method, thread)
            for run in range(5):
                base_time = (1000 / t) * (1.0 if method == "raxtax" else 0)
                noise = rng.normal(0, base_time * 0.25)  # 5% noise
                rows.append({"Threads": t, "Runtime": base_time + noise, "Method": method})

    df = pd.DataFrame(rows)

    print(df)


    plot_benchmark(
        df,
        x_col="Threads",
        y_col="Runtime",
        hue_col="Method",
        error="sd",
        xgrid_exact=True,
    )