import numpy as np
from scipy.special import comb

#calculates pmf for one query sequence
def calculate_pmf(match_count: int, reference_set_size: int, query_set_size: int, t: int) -> np.ndarray:
    # references equation 8
    pmf = np.zeros(t + 1)
    denominator = comb(query_set_size + t - 1, t)
    for m in range(0, t + 1):
        nominator1_n = match_count + m - 1
        nominator1_k = m
        nominator2_n = query_set_size - match_count + (t - m) - 1
        nominator2_k = t - m

        pmf[m] = comb(nominator1_n, nominator1_k) * comb(nominator2_n, nominator2_k) / denominator
    return pmf