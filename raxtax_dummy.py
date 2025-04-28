import numpy as np
import math
import matplotlib.pyplot as plt

#calculates pmf for one query sequence
def calculate_pmf(match_count: int, reference_set_size: int, query_set_size: int, t: int) -> np.ndarray:
    # references equation 8
    denominator = math.comb(query_set_size + t - 1, t)

    nominator1_n = match_count + 0 - 1
    nominator1_k = 0
    nominator2_n = reference_set_size - match_count + (t - 0) - 1
    nominator2_k = t - 0

    nominator = math.comb(nominator1_n, nominator1_k) * math.comb(nominator2_n, nominator2_k)

    pmf: np.ndarray = np.zeros(t + 1)
    pmf[0] = nominator / denominator

    for i in range(1, t + 1):
        nominator1_n += 1
        nominator1_k += 1

        nominator = nominator * nominator1_n * nominator2_k / (nominator1_k * nominator2_n)

        pmf[i] = nominator / denominator

        nominator2_n -= 1
        nominator2_k -= 1

    return pmf

#calculates array of pmfs
def calculate_probabilities(match_counts: np.ndarray, reference_set_sizes: np.ndarray, t: int, query_set_size: int) -> np.ndarray:
    num_queries = len(match_counts)

    pmfs: np.ndarray = np.zeros((num_queries, t + 1))

    for i in range(num_queries):
        pmfs[i, :] = calculate_pmf(match_counts[i], reference_set_sizes[i], query_set_size, t)

    return pmfs

def calculate_Ci(pmfs_prefix_sum: np.ndarray, i: int, t: int) -> np.ndarray:
    n = len(pmfs_prefix_sum)
    Ci = np.zeros(t + 1)
    for m in range(t + 1):
        Ci[m] = np.prod([pmfs_prefix_sum[j][m] for j in range(n) if i != j])
    return Ci

def calculate_C(pmfs: np.ndarray, t: int) -> np.ndarray:
    pmfs_prefix_sum = np.cumsum(np.array(pmfs), axis=1)

    C = np.zeros((len(pmfs), t + 1))
    for i in range(len(pmfs)):
        C[i, :] = calculate_Ci(pmfs_prefix_sum, i, t)

    return C

def calculate_P(pmfs: np.ndarray, C: np.ndarray, t: int) -> np.ndarray:
    n = len(pmfs)
    P = np.zeros(n)
    for i in range(n):
        P[i] = np.dot(pmfs[i], C[i])
    return P

def normalize_P(P: np.ndarray) -> np.ndarray:
    sum = np.sum(P)
    return P / sum

def calculate_confidence_scores(match_counts: np.ndarray, reference_set_sizes: np.ndarray, t: int, query_set_size: int) -> np.ndarray:
    pmfs = calculate_probabilities(match_counts, reference_set_sizes, t, query_set_size)
    C = calculate_C(pmfs, t)
    P = calculate_P(pmfs, C, t)
    normalized_P = normalize_P(P)

    return normalized_P


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
    plt.show()

def main():
    match_counts = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    reference_set_sizes = np.array([20, 20, 20, 20, 20, 20, 20, 20, 20, 20])
    t = 8
    query_set_size = 20
    confidence_scores = calculate_confidence_scores(match_counts, reference_set_sizes, t, query_set_size)

    for x in confidence_scores:
        print(x)

    print(np.sum(confidence_scores))

    plot_probabilities(confidence_scores, np.arange(1, len(match_counts) + 1))


if __name__ == "__main__":
    main()