import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_probabilities(probabilities: np.ndarray, x_labels: np.ndarray, xlabel: str = "matching k-mers",
                           ylabel: str = "Probability", title: str = "Probability matching k-mers"):
    """
    Plots a bar chart for a given array of probabilities with custom x-axis labels.

    Parameters:
    - probabilities: np.ndarray of values between 0 and 1
    - x_labels: np.ndarray or list, labels for each bar
    - xlabel: str, label for the x-axis
    - ylabel: str, label for the y-axis
    - title: str, title for the plot
    """

    # Create a figure
    plt.figure(figsize=(8, 5))

    # Plot bar chart
    plt.bar(x_labels, probabilities, color='skyblue', edgecolor='black')

    # Labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.ylim(0, 1)  # since we are plotting probabilities
    plt.grid(axis='y')
    #plt.grid(axis='x')

    # Show the plot
    #plt.show()

def plot_contour_shared_vs_matched(shared_counts, true_matches, probabilities,
                                   xlabel='Number of Shared Elements',
                                   ylabel='Number of True Matches',
                                   title='Match Probability Contour Diagram'):
    """
    Plots a contour diagram for match probabilities.

    Parameters:
    - shared_counts: 2D numpy array (x-values)
    - true_matches: 2D numpy array (y-values)
    - probabilities: 2D numpy array (z-values for contour)
    - xlabel: label for the x-axis
    - ylabel: label for the y-axis
    - title: plot title
    """
    plt.figure(figsize=(8, 6))
    levels = np.linspace(0, 0.25, 100)
    contour = plt.contourf(shared_counts, true_matches, probabilities, levels=levels, cmap='YlGnBu', extend='max')
    cbar = plt.colorbar(contour)
    cbar.set_label('Match Probability')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    #plt.show()

def plot_runtime_vs_references(references, runtimes, save_path = None):
    """
    Erstellt ein Diagramm zur Darstellung der Laufzeit in Abhängigkeit der Referenzanzahl
    und fügt eine Regressionslinie hinzu.

    :param references: Liste mit Referenzanzahlen (x-Achse)
    :param runtimes: Liste mit Laufzeiten (y-Achse)
    """

    # Überprüfen, ob die Länge der Listen übereinstimmt
    if len(references) != len(runtimes):
        raise ValueError("Die Länge der Referenzanzahlen und Laufzeiten muss gleich sein.")

    # Regressionsberechnung
    coeffs = np.polyfit(references, runtimes, deg=1)
    poly = np.poly1d(coeffs)

    # Erzeugen von x-Werten für die Regressionslinie
    x_line = np.linspace(min(references), max(references), 100)
    y_line = poly(x_line)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.scatter(references, runtimes, color='blue', label='Datapoints')
    plt.plot(x_line, y_line, color='red', linestyle='--', label='Regression line')
    plt.xlabel('Number of References')
    plt.ylabel('Create Look Up (s)')
    plt.title('Create Look Up (s) vs. Number of References')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()


def plot_runtime_vs_references_fixed_queries(references, runtimes, save_path=None):
    """
    Plots runtime as a function of the number of references, assuming a fixed number of queries (e.g., 50).

    :param references: List of reference counts (x-axis)
    :param runtimes: List of runtimes (y-axis)
    :param save_path: Optional path to save the plot (e.g., 'runtime_plot.png')
    """

    if len(references) != len(runtimes):
        raise ValueError("Length of reference list must match length of runtime list.")

    # Linear regression
    coeffs = np.polyfit(references, runtimes, 1)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(min(references), max(references), 100)
    y_line = poly(x_line)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.scatter(references, runtimes, color='blue', label='Measured runtime')
    plt.plot(x_line, y_line, color='red', linestyle='--',
             label=f'Regression line: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
    plt.title('Runtime vs. Number of References (Queries = 50)')
    plt.xlabel('Number of References')
    plt.ylabel('Runtime (s)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

def plot_runtime_vs_queries_fixed_references(queries, runtimes, save_path=None):
    """
    Plots runtime as a function of the number of queries,
    assuming the number of references is fixed (e.g., 1000).

    :param queries: List of query counts (x-axis)
    :param runtimes: List of runtimes (y-axis)
    :param save_path: Optional path to save the plot (e.g., 'runtime_vs_queries.png')
    """

    if len(queries) != len(runtimes):
        raise ValueError("Length of query list must match length of runtime list.")

    # Linear regression
    coeffs = np.polyfit(queries, runtimes, 1)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(min(queries), max(queries), 100)
    y_line = poly(x_line)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.scatter(queries, runtimes, color='blue', label='Measured runtime')
    plt.plot(x_line, y_line, color='red', linestyle='--',
             label=f'Regression line: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
    plt.title('Runtime vs. Number of Queries (References = 1000)')
    plt.xlabel('Number of Queries')
    plt.ylabel('Runtime (s)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

def plot_runtime_vs_tree_height(tree_heights, runtimes, save_path=None):
    """
    Plots runtime as a function of the tree height,
    assuming the number of references (1000) adn the number of queries (50) is fixed.

    :param tree_heights: List of tree heights (x-axis)
    :param runtimes: List of runtimes (y-axis)
    :param save_path: Optional path to save the plot (e.g., 'runtime_vs_queries.png')
    """

    if len(tree_heights) != len(runtimes):
        raise ValueError("Length of query list must match length of runtime list.")

    # Linear regression
    coeffs = np.polyfit(tree_heights, runtimes, 1)
    poly = np.poly1d(coeffs)
    x_line = np.linspace(min(tree_heights), max(tree_heights), 100)
    y_line = poly(x_line)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.scatter(tree_heights, runtimes, color='blue', label='Measured runtime')
    plt.plot(x_line, y_line, color='red', linestyle='--',
             label=f'Regression line: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
    plt.title('Runtime vs. Tree Height (References = 1000, Queries = 50)')
    plt.xlabel('Tree Height')
    plt.ylabel('Runtime (s)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

def plot_xy_data(x, y, title="My Plot", xlabel="X-Axis", ylabel="Y-Axis", mode="lines",  # "points", "lines", or "polyfit"
                 save_path=None):
    """
    Plots x and y data with optional styling.

    Parameters:
    - x, y: Arrays or lists of data points
    - title: Plot title
    - xlabel, ylabel: Axis labels
    - mode:
        - 'points' = scatter plot only
        - 'lines' = connects the points with lines
        - 'polyfit' = fits a polynomial curve (degree 1)
    - save_path: If given, saves the figure to this path instead of displaying it
    """

    if len(x) != len(y):
        raise ValueError("x and y must be the same length")

    x = np.array(x)
    y = np.array(y)

    plt.figure(figsize=(8, 5))

    if mode == "points":
        plt.scatter(x, y, color='blue')
    elif mode == "lines":
        plt.plot(x, y, marker='o', color='blue')
    elif mode == "polyfit":
        coeffs = np.polyfit(x, y, deg=1)
        poly = np.poly1d(coeffs)
        x_fit = np.linspace(min(x), max(x), 200)
        y_fit = poly(x_fit)
        plt.scatter(x, y, color='blue', label='Data points')
        plt.plot(x_fit, y_fit, color='red', linestyle='--')
    else:
        raise ValueError("Invalid mode. Choose from: 'points', 'lines', 'polyfit'")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    plt.close()

def plot_multiple_xy_array(x_data, y_data, title="My Plot", xlabel="X-Axis", ylabel="Y-Axis", mode="lines", save_path=None):
    """
    Plots multiple (x, y) datasets from 2D arrays.

    Parameters:
    - x_data: 2D array-like, shape (n_datasets, n_points)
    - y_data: 2D array-like,shape (n_datasets, n_points)
    - title: Plot title
    - xlabel, ylabel: Axis labels
    - mode: 'points', 'lines', or 'polyfit'
    - save_path: If given, saves the plot instead of showing it
    """

    n_datasets = len(x_data)
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    plt.figure(figsize=(8, 5))

    for i in range(n_datasets):
        x = x_data[i]
        y = y_data[i]
        color = color_cycle[i % len(color_cycle)]

        if len(x) != len(y):
            raise ValueError(f"x and y must have the same length in dataset {i+1}")

        if mode == "points":
            plt.scatter(x, y, color=color)
        elif mode == "lines":
            plt.plot(x, y, marker='o', color=color)
        elif mode == "polyfit":
            coeffs = np.polyfit(x, y, deg=1)
            poly = np.poly1d(coeffs)
            x_fit = np.linspace(min(x), max(x), 200)
            y_fit = poly(x_fit)
            plt.scatter(x, y, color=color, alpha=0.6)
            plt.plot(x_fit, y_fit, linestyle='--', color=color)
        else:
            raise ValueError("Invalid mode. Choose from: 'points', 'lines', 'polyfit'")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    plt.close()

def plot_mean_with_std_band(
    x_data,
    y_data,
    title="My Plot",
    xlabel="X-Axis",
    ylabel="Y-Axis",
    ref_y_intercept=None,       # float | None
    ref_slope=None,             # float | None
    ref_label="ideal",          # str label for legend
    use_sample_std=True,        # ddof=1 (sample std) instead of ddof=0
    save_path=None
):
    """
    Plots the mean across multiple (x, y) datasets with a shaded ±1 std deviation band.

    Parameters
    ----------
    x_data : array-like, shape (n_datasets, n_points) or (n_points,)
        x values. Can be a shared 1D array or per dataset (2D, must be identical).
    y_data : array-like, shape (n_datasets, n_points)
        y values for each dataset.
    dashed_ref : float | None
        Optional: horizontal dashed reference line (e.g., 1.0).
    use_sample_std : bool
        True -> ddof=1 (sample std), False -> ddof=0 (population std).
    save_path : str | Path | None
        If given, saves the plot to file, otherwise displays it.
    """

    # Convert to NumPy arrays
    y = np.asarray(y_data)
    x = np.asarray(x_data)

    # Handle x values: either 1D (shared) or 2D (identical for all datasets)
    if x.ndim == 1:
        x_ref = x
        if y.shape[-1] != x_ref.shape[0]:
            raise ValueError("x and y must have the same number of points.")
    elif x.ndim == 2:
        # Ensure all x rows are identical
        x_first = x[0]
        if not np.allclose(x, x_first, atol=0, rtol=0):
            raise ValueError("All x arrays must be identical.")
        x_ref = x_first
    else:
        raise ValueError("x_data must be 1D (shared x) or 2D (n_datasets, n_points).")

    if y.ndim != 2:
        raise ValueError("y_data must be 2D: (n_datasets, n_points).")

    if y.shape[1] != x_ref.shape[0]:
        raise ValueError("x and y must have the same number of points per dataset.")

    # Compute mean and standard deviation across datasets
    ddof = 1 if use_sample_std else 0
    y_mean = np.mean(y, axis=0)
    y_std  = np.std(y, axis=0, ddof=ddof)

    # Plot
    plt.figure(figsize=(8, 5))
    # Shaded band for ±1 standard deviation
    plt.fill_between(x_ref, y_mean - y_std, y_mean + y_std, alpha=0.2, label="±1 SD")
    # Mean line
    plt.plot(x_ref, y_mean, marker='o', linewidth=2, label="Mean")

    # Optional dashed reference line: y = m * x + b
    if (ref_y_intercept is not None) and (ref_slope is not None):
        # build a smooth x-grid over current x-range
        x_min, x_max = np.min(x_ref), np.max(x_ref)
        #x_min, x_max = plt.gca().get_xlim()
        x_line = np.linspace(x_min, x_max, 200)
        y_line = ref_slope * x_line + ref_y_intercept
        plt.plot(x_line, y_line, label=ref_label, linewidth=1.5, linestyle="--")
        #plt.axline((0, ref_y_intercept), slope=ref_slope, label=ref_label, linewidth=1.5, linestyle="--")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    if save_path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()

    plt.close()

if __name__ == "__main__":
    x_data = [[0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22],
              [0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22],
              [0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22],
              [0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22],
              [0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22]]
    y_data = [
        [2688.8539166250002, 4094.335515292, 3745.266366334, 2944.983916916999, 3508.0587890000006, 3746.8269063340013,
         3004.7424787089985, 3428.402953375, 4675.311673624998, 3530.522442290996],
        [3573.1002347500003, 4556.950297250001, 3319.9995624169987, 2975.3156988329993, 9753.738445792,
         22096.401757666998, 4376.646825000003, 4042.7587859999985, 4045.274622750003, 2559.508381917003],
        [2950.644497584, 5354.978489249999, 4685.975270792, 2678.016649416999, 5768.782542792002, 3679.9870832919987,
         2958.0853260839976, 4530.204249583003, 3201.6168309579953, 3804.681532415998],
        [3217.093067625, 8486.419032125, 3296.3088194580014, 2652.013246042001, 7233.894556040999, 4043.3927685419985,
         3119.8281305419987, 5127.230851166001, 3173.8501854169954, 3911.5875649160007],
        [5867.4894365, 2646.791423375, 2798.233308375, 4031.2248027080004, 4240.501207249999, 2882.176224249997,
         3486.8702652499996, 5282.552250416, 6069.935950666, 2546.251856584]]

    plot_mean_with_std_band(x_data, y_data, ref_slope=1000, ref_y_intercept=0)