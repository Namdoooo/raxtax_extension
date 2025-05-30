import matplotlib.pyplot as plt
import numpy as np

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