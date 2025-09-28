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

def compare_sequences(str1: str, str2: str) -> int:
    if len(str1) != len(str2):
        raise ValueError()

    count = 0

    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count

def compare_files(file1: str, file2: str) -> bool:
    """
    Compare two text files line by line.

    Prints how many lines each file has, and for the overlapping part,
    prints differing lines with their line numbers.

    Args:
        file1: Path to the first file.
        file2: Path to the second file.

    Returns:
        True if files are identical, False otherwise.
    """
    with open(file1, "r", encoding="utf-8") as f1:
        lines1 = f1.readlines()
    with open(file2, "r", encoding="utf-8") as f2:
        lines2 = f2.readlines()

    len1, len2 = len(lines1), len(lines2)
    print(f"{file1}: {len1} lines")
    print(f"{file2}: {len2} lines")

    identical = True
    if len1 != len2:
        identical = False

    min_len = min(len1, len2)

    for lineno in range(min_len):
        if lines1[lineno] != lines2[lineno]:
            print(f"Difference at line {lineno + 1}:")
            print(f"  {file1}: {lines1[lineno].rstrip()}")
            print(f"  {file2}: {lines2[lineno].rstrip()}")
            identical = False

    if len1 != len2:
        print("\n Files have different lengths.")
        if len1 > len2:
            for lineno in range(min_len, len1):
                print(f"Extra line in {file1} at {lineno + 1}: {lines1[lineno].rstrip()}")
        else:
            for lineno in range(min_len, len2):
                print(f"Extra line in {file2} at {lineno + 1}: {lines2[lineno].rstrip()}")
        identical = False

    if identical:
        print("Files have identical lines.")
    else:
        print("Files dont have identical lines.")

    return identical


def float_to_string_without_point(num: float) -> str:
    # Erst als String mit möglichst wenig Nachkommastellen darstellen
    s = format(num, 'f').rstrip('0').rstrip('.')
    return s.replace(".", "")


def create_folder(path: Union[Path, str]) -> None:

    folder_path = Path(path)
    folder_path.mkdir(parents=True, exist_ok=True)

    #print(f"[INFO] directory created or existed: {folder_path.resolve()}")

if __name__ == "__main__":
    file1 = "../experiments/small_test/test1/results_references_queries_200/results.out"
    file2 = "../experiments/small_test/test2/results_references_queries_200/results.out"
    compare_files(file1, file2)

    file1 = "../experiments/small_test/test1/queries.fasta"
    file2 = "../experiments/small_test/test2//queries/queries.fasta"
    compare_files(file1, file2)
