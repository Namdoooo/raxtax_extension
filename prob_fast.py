import numpy as np
from scipy.special import comb

#calculates pmf for one query sequence
def calculate_pmf(match_count: int, query_set_size: int, t: int) -> np.ndarray:
    print(match_count)
    # references equation 8

    pmf: np.ndarray = np.zeros(t + 1)
    if match_count == 0:
        pmf[0] = 1
        return pmf

    if match_count == query_set_size:
        pmf[0] = 1e-300
        pmf[-1] = 1
        return pmf

    denominator = comb(query_set_size + t - 1, t)

    nominator1_n = match_count + 0 - 1
    nominator1_k = 0

    nominator2_n = query_set_size - match_count + (t - 0) - 1
    nominator2_k = t - 0

    nominator = comb(nominator1_n, nominator1_k) * comb(nominator2_n, nominator2_k)

    pmf[0] = nominator / denominator
    print("denominator: ", denominator)

    if pmf[0] == 0:
        print(0, match_count, query_set_size)

    for i in range(1, t + 1):
        nominator1_n += 1
        nominator1_k += 1
        print("nominator: ", nominator)
        nominator = nominator / nominator1_k  * nominator1_n / nominator2_n  * nominator2_k

        pmf[i] = nominator / denominator

        if pmf[i] == 0:
            print(i, match_count, query_set_size)

        nominator2_n -= 1
        nominator2_k -= 1

    if np.any(pmf == 0.0):
        raise ValueError("PMF contains zero entries, which is not allowed.")

    return pmf

def calculate_confidence_scores(match_counts: np.ndarray, t: int, query_set_size: int) -> np.ndarray:
    #calculate number of occurrences of each match_count
    occurrences = {}
    for match_count in match_counts:
        if match_count in occurrences:
            occurrences[match_count] += 1
        else:
            occurrences[match_count] = 1

    #calculate pmf for each match_count
    pmf_dict = {key: calculate_pmf(key, query_set_size, t) for key in occurrences}
    #print("pmf_dict", pmf_dict)

    #calculate pmf_prefix_sum for each match_count
    pmf_prefix_sum_dict = {
        key : np.cumsum(pmf, axis=0, dtype=np.float64)
        for key, pmf in pmf_dict.items()
    }
    #print("pmf_prefix_sum_dict", pmf_prefix_sum_dict)

    #calculate log of pmf_prefix_sum for each match_count
    log_pmf_prefix_sum_dict = { key : np.log(pmf_prefix_sum_dict[key]) for key in pmf_prefix_sum_dict}
    #print("log_pmf_prefix_sum_dict", log_pmf_prefix_sum_dict)

    scaled_log_prefix_sum_dict = {
        key : occurrences[key] * log_pmf_prefix_sum_dict[key] for key in occurrences
    }

    #calculate log of C
    log_C = np.sum(np.stack(list(scaled_log_prefix_sum_dict.values())), axis=0, dtype=np.float64)
    #print("log_C", log_C)

    #calculate C
    C = np.exp(log_C)
    #print("C", C)

    #calculate probabilities for each match_count
    P_dict = {
        key : np.sum(pmf_dict[key] * (C / pmf_prefix_sum_dict[key]), dtype=np.float64) for key in occurrences
    }

    #print("P_dict", P_dict)

    P = np.array([P_dict[match_count] for match_count in match_counts])

    sum = np.sum(P)
    normalized_P = P / sum

    return normalized_P






