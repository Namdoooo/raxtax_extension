import numpy as np
from scipy.special import comb


#calculates pmf for one query sequence
def calculate_pmf(match_count: int, reference_set_size: int, query_set_size: int, t: int) -> np.ndarray:
    # references equation 8

    pmf: np.ndarray = np.zeros(t + 1)
    if match_count == 0:
        pmf[0] = 1
        return pmf

    denominator = comb(query_set_size + t - 1, t)

    nominator1_n = match_count + 0 - 1
    nominator1_k = 0
    #nominator2_n = reference_set_size - match_count + (t - 0) - 1
    nominator2_n = query_set_size - match_count + (t - 0) - 1
    nominator2_k = t - 0

    nominator = comb(nominator1_n, nominator1_k) * comb(nominator2_n, nominator2_k)

    pmf[0] = nominator / denominator

    if pmf[0] == 0:
        print(0, match_count, reference_set_size, query_set_size)

    for i in range(1, t + 1):
        nominator1_n += 1
        nominator1_k += 1

        nominator = nominator / nominator1_k  * nominator1_n / nominator2_n  * nominator2_k

        pmf[i] = nominator / denominator

        if pmf[i] == 0:
            print(i, match_count, reference_set_size, query_set_size)

        nominator2_n -= 1
        nominator2_k -= 1

    if np.any(pmf == 0.0):
        raise ValueError("PMF contains zero entries, which is not allowed.")

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
    #pmfs_sum = np.sum(pmfs, axis=1)
    #print("pmfs_sum: ")
    #print(pmfs_sum)

    pmfs_prefix_sum = np.cumsum(np.array(pmfs), axis=1, dtype=np.float64)

    #print("pmfs_prefix_sum: ")
    #print(pmfs_prefix_sum)

    #print("Last three elements of each row:")
    #print(pmfs_prefix_sum[:, -3:])

    #print(pmfs_prefix_sum[:, -2])
    #for x in pmfs_prefix_sum[:, -2]:
    #    print(x)
    #print("Produkt der vorletzten Spalte (sollte ≈ 1 sein):")
    #print(np.prod(pmfs_prefix_sum[:, -2]))

    log_C = np.sum(np.log(pmfs_prefix_sum), axis=0, dtype=np.float64)

    #print("log_C: ")
    #print(log_C)

    C1 = np.exp(log_C)
    C = np.prod(pmfs_prefix_sum, axis=0, dtype=np.float64)
    #print("C1: ")
    #print(C1)
    #print("C: ")
    #print(C)

    #pmfs_prefix_sum[pmfs_prefix_sum == 0.0] = 1e-300

    num_rows = pmfs_prefix_sum.shape[0]
    half = num_rows // 2



    # Erste Hälfte
    #C_first = np.prod(pmfs_prefix_sum[:half, :], axis=0, dtype=np.float64)

    # Zweite Hälfte
    #C_second = np.prod(pmfs_prefix_sum[half:, :], axis=0, dtype=np.float64)
    #print("C_first: ")
    #print(C_first)
    #print("C_second: ")
    #print(C_second)

    P = np.sum(pmfs * (C / pmfs_prefix_sum), axis=1, dtype=np.float64)
    return P

def normalize_P(P: np.ndarray) -> np.ndarray:
    sum = np.sum(P, dtype=np.float64)
    return P / sum

def calculate_confidence_scores(match_counts: np.ndarray, reference_set_sizes: np.ndarray, t: int, query_set_size: int) -> np.ndarray:
    pmfs = calculate_probabilities(match_counts, reference_set_sizes, t, query_set_size)

    #print("pmfs:")
    #print(pmfs)

    P = calculate_P(pmfs)
    #print("P:")
    #print(P)

    normalized_P = normalize_P(P)
    #print("normalized_P:")
    #print(normalized_P)

    return normalized_P
