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

        nominator = nominator / nominator1_k  * nominator1_n / nominator2_n  * nominator2_k

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

#calculate array P with the cashed C
def calculate_P(pmfs: np.ndarray) -> np.ndarray:
    pmfs_prefix_sum = np.cumsum(np.array(pmfs), axis=1)
    C = np.prod(pmfs_prefix_sum, axis=0)

    P = np.sum(pmfs * (C / pmfs_prefix_sum), axis=1)
    return P

def normalize_P(P: np.ndarray) -> np.ndarray:
    sum = np.sum(P)
    return P / sum

def calculate_confidence_scores(match_counts: np.ndarray, reference_set_sizes: np.ndarray, t: int, query_set_size: int) -> np.ndarray:
    pmfs = calculate_probabilities(match_counts, reference_set_sizes, t, query_set_size)
    P = calculate_P(pmfs)
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

def test0():
    match_counts = np.array([3, 7, 12, 20, 30])
    reference_set_sizes = np.array([200, 200, 200, 200, 200])
    t = 8
    query_set_size = 200
    confidence_scores = calculate_confidence_scores(match_counts, reference_set_sizes, t, query_set_size)

    for x in confidence_scores:
        print(x)

    print(np.sum(confidence_scores))

    plot_probabilities(confidence_scores, np.arange(1, len(match_counts) + 1))

    plt.show()

def test1():
    match_count = np.array([13, 20, 29])
    reference_set_size = np.array([200, 200, 200])
    query_set_size = 200
    t = 32

    calculated_pmfs = calculate_probabilities(match_count, reference_set_size, t, query_set_size)
    #print(calculated_pmfs)
    plot_contour_shared_vs_matched(match_count, np.arange(t + 1), calculated_pmfs.T)

    real_pmfs = np.array([
        [0.136016559872931, 0.25955453627128255, 0.25955453627128255, 0.1802462057439474, 0.09724911565719903, 0.04326222341385706, 0.016451831439072417, 0.005476553053168284, 0.001622201733758381, 0.00043258712900223637, 0.00010473162070580414, 2.3161800733014587e-5, 4.699495800901472e-6, 8.774264004670411e-7, 1.5102740133474437e-7, 2.3986704917871156e-8, 3.515292962101802e-9, 4.7498425579943e-10, 5.907764375614835e-11, 6.747288786886374e-12, 7.052442551117421e-13, 6.716611953445226e-14, 5.7960610765771195e-15, 4.500047419702709e-16, 3.115417444409562e-17, 1.9013681722582056e-18, 1.0078994296944639e-19, 4.549546036815298e-21, 1.7014009112996629e-22, 5.064060788623342e-24, 1.1253468419162924e-25, 1.660601036458504e-27, 1.2210301738664155e-29],
        [0.044017985555600984, 0.1335142689838149, 0.20694711692491233, 0.21783907044727566, 0.1746378124859777, 0.11338802897640253, 0.061923074076919334, 0.029170730366548676, 0.012065099875870353, 0.004437737885377524, 0.001465332262151888, 0.00043741261556772963, 0.00011864817197274797, 2.9352466201220585e-5, 6.6392483074189305e-6, 1.3750321367649388e-6, 2.6088779380585136e-7, 4.5330729783459995e-8, 7.204626297199366e-9, 1.0452307581429133e-9, 1.3800312353605594e-10, 1.6514958687934853e-11, 1.7818771215929838e-12, 1.7216204073362232e-13, 1.4766558015051454e-14, 1.1118349564274048e-15, 7.24210114298245e-17, 4.0016414723987e-18, 1.8252828921073316e-19, 6.6036238041192375e-21, 1.777898716493646e-22, 3.1685951104859196e-24, 2.80552692074305e-26],
        [0.009707738857520212, 0.04459792900880548, 0.10317431337858017, 0.15992018573680092, 0.1864396135223001, 0.17401030595414857, 0.13514505995423706, 0.08963702956148284, 0.051713670900855796, 0.02630111097363076, 0.011910451290649375, 0.004838620836826296, 0.0017733165370567726, 0.0005887123726261319, 0.00017754817587137386, 4.8731307845547066e-5, 1.2182826961386723e-5, 2.774078245477054e-6, 5.748090058195745e-7, 1.0818773622118926e-7, 1.8445122240989473e-8, 2.837711113998407e-9, 3.9194904889480236e-10, 4.8283578487040685e-11, 5.259942907806158e-12, 5.011720882943355e-13, 4.11653736147889e-14, 2.858706501027012e-15, 1.6335465720154425e-16, 7.381066556074497e-18, 2.4745772268920367e-19, 5.47637120730043e-21, 6.004792990460901e-23]
    ])

    plot_contour_shared_vs_matched(match_count, np.arange(t + 1), real_pmfs.T)

    #print(np.allclose(calculated_pmfs, real_pmfs, rtol=1e-12, atol=1e-20))
    assert np.allclose(calculated_pmfs, real_pmfs, rtol=1e-12, atol=1e-20)

    """
    for row in range(3):
        for col in range(t + 1):
            print(f"{real_pmfs[row][col]:.16e} : {calculated_pmfs[row][col]:.16e}")
    """

    plt.show()


def main():
    #test0()
    test1()

if __name__ == "__main__":
    main()