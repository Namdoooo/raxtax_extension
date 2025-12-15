"""
prob_fast.py

Purpose
-------
Probabilistic model of raxtax.
"""

import numpy as np
from scipy import special

#calculates pmf for one query sequence
def calculate_pmf_old(match_count: int, query_set_size: int, t: int) -> np.ndarray:
    #print(match_count)
    # references equation 8

    pmf: np.ndarray = np.zeros(t + 1)
    if match_count == 0:
        pmf[0] = 1
        return pmf

    if match_count == query_set_size:
        pmf[0] = 1e-300
        pmf[-1] = 1
        return pmf

    denominator = special.comb(query_set_size + t - 1, t)

    nominator1_n = match_count + 0 - 1
    nominator1_k = 0

    nominator2_n = query_set_size - match_count + (t - 0) - 1
    nominator2_k = t - 0

    nominator = special.comb(nominator1_n, nominator1_k) * special.comb(nominator2_n, nominator2_k)

    pmf[0] = nominator / denominator
    #print("denominator: ", denominator)

    if pmf[0] == 0:
        print(0, match_count, query_set_size)

    for i in range(1, t + 1):
        nominator1_n += 1
        nominator1_k += 1
        #print("nominator: ", nominator)
        nominator = nominator / nominator1_k  * nominator1_n / nominator2_n  * nominator2_k

        pmf[i] = nominator / denominator

        if pmf[i] == 0:
            print(i, match_count, query_set_size)

        nominator2_n -= 1
        nominator2_k -= 1

    if np.any(pmf == 0.0):
        raise ValueError("PMF contains zero entries, which is not allowed.")

    return pmf

def log_binom(n: int, k: int):
    """
    Computes the natural logarithm of the binomial coefficient C(n, k).

    The computation is performed using the log-gamma function to ensure
    numerical stability for large values of n and k.

    Parameters
    ----------
    n : int
        Total number of elements.
    k : int
        Number of selected elements.

    Returns
    -------
    float
        Natural logarithm of the binomial coefficient.

    Raises
    ------
    ValueError
        If k is not in the range [0, n].
    """
    if k < 0 or k > n:
        raise ValueError("k must be between 0 and n")
    return special.gammaln(n + 1) - special.gammaln(k + 1) - special.gammaln(n - k + 1)

def calculate_pmf(match_count: int, query_set_size: int, t: int) -> np.ndarray:
    """
    Computes the probability mass function (PMF) for a single
    query–reference pair.

    Parameters
    ----------
    match_count : int
        Size of the intersection between the query and reference k-mer
        sets.
    query_set_size : int
        Size of the query k-mer set.
    t : int
        Subsample size.

    Returns
    -------
    numpy.ndarray
        Probability mass function of length t + 1.
    """
    pmf_log = np.full(t + 1, -np.inf)

    if match_count == 0:
        pmf_log[0] = 0
    elif match_count == query_set_size:
        pmf_log[0] = -700       # ~log(1e-300)
        pmf_log[-1] = 0
    else:
        log_denominator = log_binom(query_set_size + t - 1, t)

        nominator1_n = match_count + 0 - 1
        nominator1_k = 0

        nominator2_n = query_set_size - match_count + (t - 0) - 1
        nominator2_k = t - 0

        log_nominator = log_binom(nominator1_n, nominator1_k) + log_binom(nominator2_n, nominator2_k)
        pmf_log[0] = log_nominator - log_denominator

        for i in range(1, t + 1):
            nominator1_n += 1
            nominator1_k += 1
            log_nominator = log_nominator - np.log(nominator1_k)  + np.log(nominator1_n) - np.log(nominator2_n)  + np.log(nominator2_k)

            pmf_log[i] = log_nominator - log_denominator

            nominator2_n -= 1
            nominator2_k -= 1



    pmf = np.exp(pmf_log - np.max(pmf_log))

    if pmf[0] == 0:
        pmf[0] = 1e-300

    pmf /= np.sum(pmf)
    return pmf

def calculate_confidence_scores(match_counts: np.ndarray, t: int, query_set_size: int) -> np.ndarray:
    """
    Computes confidence scores for a single query with respect
    to all reference sequences.

    Parameters
    ----------
    match_counts : numpy.ndarray
        Array of k-mer intersection sizes between the query and each
        reference sequence.
    t : int
        Subsample size.
    query_set_size : int
        Size of the query k-mer set.

    Returns
    -------
    numpy.ndarray
        Confidence scores for the query across all references.
    """
    #calculate number of occurrences of each match_count
    occurrences = {}
    for match_count in match_counts:
        if match_count in occurrences:
            occurrences[match_count] += 1
        else:
            occurrences[match_count] = 1

    #calculate pmf for each match_count
    pmf_dict = {key: calculate_pmf(key, query_set_size, t) for key in occurrences}

    #calculate pmf_prefix_sum for each match_count
    pmf_prefix_sum_dict = {
        key : np.cumsum(pmf, axis=0, dtype=np.float64)
        for key, pmf in pmf_dict.items()
    }

    #calculate log of pmf_prefix_sum for each match_count
    log_pmf_prefix_sum_dict = { key : np.log(pmf_prefix_sum_dict[key]) for key in pmf_prefix_sum_dict}

    #weight each log-prefix-sum by its corresponding occurrence count
    scaled_log_prefix_sum_dict = {
        key : occurrences[key] * log_pmf_prefix_sum_dict[key] for key in occurrences
    }

    #calculate log of C
    log_C = np.sum(np.stack(list(scaled_log_prefix_sum_dict.values())), axis=0, dtype=np.float64)

    #calculate C
    C = np.exp(log_C)

    #calculate probabilities for each match_count
    P_dict = {
        key : np.sum(pmf_dict[key] * (C / pmf_prefix_sum_dict[key]), dtype=np.float64) for key in occurrences
    }

    P = np.array([P_dict[match_count] for match_count in match_counts])

    sum = np.sum(P)
    normalized_P = P / sum

    return normalized_P






