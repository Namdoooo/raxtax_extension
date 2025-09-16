import numpy as np
import re
from pathlib import Path
from typing import Union

def kmer_to_index(kmer: str) -> int:
    base_to_bits = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    index = 0
    for base in kmer:
        if base not in base_to_bits:
            return -1
        index = (index << 2) | base_to_bits[base]
    return index

def sequence_to_kmer_set(seq: str, k: int = 8) -> list[int]:
    kmer_set = set()

    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k]
        index = kmer_to_index(kmer)
        if index != -1:
            kmer_set.add(index)

    return sorted(kmer_set)

def create_random_seed() -> int:
    seed = np.random.randint(0, 2 ** 32 - 1)
    return seed

def extract_trailing_number(value: Union[str, Path]) -> float:
    """
    Extracts the trailing number from a string.
    Leading zeros are interpreted as decimal (e.g. 'tree_height001' → 0.01).
    Raises ValueError if no number is found at the end.
    """
    s = str(value)
    match = re.search(r"(\d+)$", s)
    if not match:
        raise ValueError(f"No trailing number found in string: '{s}'")

    number_str = match.group(1)

    if number_str.startswith("0") and len(number_str) > 1:
        decimal_value = float("0." + number_str[1:])
        #print(f"Extracted (decimal): {decimal_value} from '{s}'")
        return decimal_value
    else:
        int_value = float(number_str)
        #print(f"Extracted (integer): {int_value} from '{s}'")
        return int_value

def sort_lists_by_first(a: list, b: list) -> (list, list):
    """
    Sorts two lists based on the values in the first list.

    Returns:
        A tuple of two lists, both sorted according to the order of the first list.

    Raises:
        ValueError: if the input lists are not of equal length.
    """
    if len(a) != len(b):
        raise ValueError("Both input lists must be of the same length.")

    sorted_pairs = sorted(zip(a, b))
    a_sorted, b_sorted = zip(*sorted_pairs)
    return list(a_sorted), list(b_sorted)

if __name__ == "__main__":
    pass