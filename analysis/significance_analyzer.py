"""
config_handler.py

Purpose
-------
Provides functions for significance analysis.
"""

import pandas as pd
import pingouin as pg
from pathlib import Path


def calculate_effect_size(x: pd.Series, y: pd.Series) -> float:
    """
    Calculates Cohen's d for paired samples.
    """
    differences = x - y
    return differences.mean() / differences.std()


def perform_significance_test(
    df: pd.DataFrame,
    id_col: str,
    value_col: str,
    condition_col: str,
    group_names: tuple[str, str],
    alternative: str = "two-sided"
) -> tuple[float, float]:
    """
    Performs Wilcoxon signed-rank test and computes effect size for paired samples.

    Parameters:
        df: Input DataFrame
        id_col: Column identifying each pair (e.g., dataset or DB name)
        value_col: Column containing the measured values (e.g., F1 score)
        condition_col: Column that distinguishes the two conditions
        group_names: Tuple with the two values in condition_col (e.g., ("raxtax", "sintax"))
        alternative: 'two-sided', 'greater', or 'less'

    Returns:
        Tuple with (p-value, effect size)
    """
    x = df[df[condition_col] == group_names[0]].sort_values(by=id_col)[value_col].values
    y = df[df[condition_col] == group_names[1]].sort_values(by=id_col)[value_col].values
    print("x:")
    print(x)
    print("y:")
    print(y)

    if len(x) != len(y):
        raise ValueError("Unequal number of samples for each group")

    # Wilcoxon test
    test = pg.wilcoxon(x, y, alternative=alternative)
    print(test)
    pval = test["p-val"].values[0]

    # Effect size
    effect_size = calculate_effect_size(pd.Series(x), pd.Series(y))

    return pval, effect_size


def run_significance_analysis(
    df: pd.DataFrame,
    id_col: str,
    value_col: str,
    condition_col: str,
    group_names: tuple[str, str],
    output_path: str | Path,
    alternative: str = "two-sided"
):
    """
    Run significance test and save results to file.

    Parameters:
        df: DataFrame with paired data
        id_col: Column to group by
        value_col: Measurement column
        condition_col: Grouping column (e.g., classifier)
        group_names: Tuple of condition values (e.g., ("raxtax", "sintax"))
        output_path: Path to save results TSV
        alternative: Type of Wilcoxon test
    """
    pval, effect = perform_significance_test(
        df, id_col, value_col, condition_col, group_names, alternative
    )

    results = pd.DataFrame({
        "metric": ["condition_1", "condition_2", "p_value", "effect_size"],
        "value": [group_names[0], group_names[1], pval, effect]
    })

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, sep="\t", index=False)
    print(f"Saved results to {output_path}")
