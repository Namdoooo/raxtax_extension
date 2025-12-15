"""
config_handler.py

Purpose
-------
Provides utility functions for visualizing evaluation results.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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

def plot_paired_boxplot(
    df: pd.DataFrame,
    value_col: str,
    condition_col: str,
    title: str = None,
    ylabel: str = "Value",
    save_path: str | Path = None,
    palette: list | dict | str | None = ["#ED6D52", "#58BBCC"],
    ylim: tuple[float, float] = None
):
    """
    Plots side-by-side boxplots for paired data (e.g., two methods or classifiers).

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe with one column for values and one for conditions/groups.
    value_col : str
        Name of the column containing numeric values.
    condition_col : str
        Name of the column identifying the two conditions (e.g., "method").
    title : str, optional
        Plot title.
    ylabel : str
        Y-axis label.
    save_path : str or Path, optional
        If provided, saves the plot to this path.
    palette : list, dict, str, or None
        Seaborn color palette.
    ylim : tuple(float, float) or None, default=(0, 1)
        Y-axis limits. Set to None to disable fixed range.
    """
    sns.set_style("whitegrid")
    plt.figure(figsize=(6, 5))

    ax = sns.boxplot(
        data=df,
        x=condition_col,
        y=value_col,
        hue=condition_col,
        palette=palette,
        width=0.5,
    )

    """
    sns.stripplot(
        data=df,
        x=condition_col,
        y=value_col,
        color="black",
        size=5,
        jitter=True,
        alpha=0.6
    )"""

    ax.set_xlabel(None)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    if ylim is not None:
        ax.set_ylim(*ylim)

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Saved boxplot to {save_path}")
    else:
        plt.show()

def plot_grouped_boxplots(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    hue_col: str,
    title: str = None,
    ylabel: str = "Value",
    xlabel: str = "Metric",
    ylim: tuple[float, float] = None,
    palette: list | dict | str | None = ["#ED6D52", "#58BBCC"],
    save_path: str | Path = None
):
    """
    Plot grouped boxplots comparing metrics between methods.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe (long format).
    x_col : str
        Column for x-axis grouping (e.g., metrics).
    y_col : str
        Column for y-axis values.
    hue_col : str
        Column that distinguishes the groups (e.g., method).
    title : str, optional
        Plot title.
    ylabel : str
        Label for y-axis.
    xlabel : str
        Label for x-axis.
    ylim : tuple(float, float) or None
        Y-axis limits.
    palette : list, dict, or str
        Colors for the hue groups.
    save_path : str or Path
        If provided, saves the figure.
    """
    sns.set_style("whitegrid")
    plt.figure(figsize=(8, 5))

    ax = sns.boxplot(
        data=df,
        x=x_col,
        y=y_col,
        hue=hue_col,
        palette=palette,
        #showmeans=True,
        meanprops={"marker": "o", "markerfacecolor": "black", "markeredgecolor": "black"}
    )

    """
    sns.stripplot(
        data=df,
        x=x_col,
        y=y_col,
        hue=hue_col,
        dodge=True,
        palette="dark:black",
        size=4,
        jitter=True,
        alpha=0.5,
        legend=False
    )"""

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    if ylim:
        ax.set_ylim(*ylim)

    # Move legend outside
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[:len(set(df[hue_col]))],
        labels[:len(set(df[hue_col]))],
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=len(set(df[hue_col])),
        frameon=False
    )

    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()
