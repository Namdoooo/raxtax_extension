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

    #plt.ylim(0, 0.7)
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

def plot_paired_lines(
    df: pd.DataFrame,
    id_col: str,
    value_col: str,
    condition_col: str,
    xlabel: str = None,
    ylabel: str = None,
    title: str = None,
    color: str = "#ED6D52",
    linewidth: float = None,
    alpha: float = None,
    marker: str = "o",
    markersize: int = None,
    rotation: int = 0,
    save_path: str | Path = None
):
    """
    Paired line plot using seaborn styling for consistency across plots.
    All lines and points are in the same color.
    """

    # Prepare x-axis mapping
    conditions = sorted(df[condition_col].unique())
    cond_map = {cond: i for i, cond in enumerate(conditions)}
    df["_x"] = df[condition_col].map(cond_map)

    sns.set_style("whitegrid")
    plt.figure(figsize=(6, 4))

    # Plot one line per ID (each pair)
    for _, group in df.groupby(id_col):
        if len(group) == 2:
            sns.lineplot(
                data=group,
                x="_x",
                y=value_col,
                sort=False,
                linewidth=linewidth,
                alpha=alpha,
                marker=marker,
                markersize=markersize,
                color=color
            )

    plt.xticks([0, 1], conditions, rotation=rotation)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title:
        plt.title(title)

    plt.grid(True, axis="y")
    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Saved plot to {save_path}")
    else:
        plt.show()

if __name__ == "__main__":
    df = pd.DataFrame({
        "DB": ["db1", "db1", "db2", "db2", "db3", "db3"],
        "F1": [0.87, 0.91, 0.85, 0.89, 0.83, 0.88],
        "Classifier": ["sintax", "raxtax"] * 3
    })

    plot_paired_lines(df, id_col="DB", value_col="F1", condition_col="Classifier", ylabel="F1 Score")