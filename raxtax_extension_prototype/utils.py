import subprocess

import numpy as np
import re
from pathlib import Path
from typing import Union
import random
import raxtax_extension_prototype.constants as constants

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

def complement_sequence_str(sequence: str) -> str:
    complement_table = str.maketrans("ACGTacgt", "TGCAtgca")
    return sequence.translate(complement_table)

def complement_kmer_index(kmer: int, k: int = constants.K):
    mask = (1 << (2 * k)) - 1
    return kmer ^ mask


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

def generate_unique_numbers(n, count, seed=None):
    if seed is not None:
        random.seed(seed)
    if count > n:
        raise ValueError("Count cannot be greater than the size of the range.")
    return sorted(random.sample(range(n), count))

def create_tar_archive(output_path: Path, input_paths:list[Path]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["tar", "-czvf", output_path] + input_paths
    subprocess.run(cmd, check=True)
    print(f"archive created at {output_path}")

    if output_path.exists():
        for input_path in input_paths:
            subprocess.run(["rm", "-rf", str(input_path)])

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent
    base_dir = base_dir.parent / "benchmarks_hits"

    for k in ["alternation", "alternation_m004", "alternation_m008", "alternation_t003"]:
        for i  in range(1, 31):
            for j in ["oriented", "disoriented"]:
                dir = base_dir / k / f"iteration{i}" / j
                output_path = dir / "dataset.tgz"
                input_paths = [dir / "queries/", dir / "references/"]
                create_tar_archive(output_path, input_paths)

    for j in [0, 1, 2, 4, 8, 16, 24, 32, 40, 48]:
        for i in range(1, 6):
            dir = base_dir / "core_count_benchmark" / f"iteration{i}" / f"core{j}"
            output_path = dir / "dataset.tgz"
            input_paths = [dir / "queries/", dir / "references/"]
            create_tar_archive(output_path, input_paths)

    for i in range(1, 6):
        for j in range(1, 11):
            dir = base_dir / "missing_queries" / f"iteration{i}" / f"iteration{j}"
            output_path = dir / "dataset.tgz"
            input_paths = [dir / "queries/", dir / "references/"]
            create_tar_archive(output_path, input_paths)

    for i in range(1, 6):
        for j in ["m0", "m001", "m002", "m003", "m004", "m005", "m006", "m007", "m008", "m009"]:
            dir = base_dir / "mutation_rate" / f"iteration{i}" / j
            output_path = dir / "dataset.tgz"
            input_paths = [dir / "queries/", dir / "references/"]
            create_tar_archive(output_path, input_paths)

    for k in ["query_count_benchmark", "query_memory_benchmark"]:
        for i in range(1, 6):
            for j in [100, 200, 300, 400, 500, 600, 800]:
                dir = base_dir / k / f"iteration{i}" / f"query_count{j}"
                output_path = dir / "dataset.tgz"
                input_paths = [dir / "queries/", dir / "references/"]
                create_tar_archive(output_path, input_paths)

    for k in ["reference_count_benchmark", "reference_memory_benchmark"]:
        for i in range(1, 6):
            for j in [400, 800, 1200, 1600, 2000, 2400, 2800, 3200]:
                dir = base_dir / k / f"iteration{i}" / f"leaf_count{j}"
                output_path = dir / "dataset.tgz"
                input_paths = [dir / "queries/", dir / "references/"]
                create_tar_archive(output_path, input_paths)

    for i in range(1, 6):
        for j in [20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000]:
            dir = base_dir / "sequence_length_benchmark" / f"iteration{i}" / f"sequence_length{j}"
            output_path = dir / "dataset.tgz"
            input_paths = [dir / "queries/", dir / "references/"]
            create_tar_archive(output_path, input_paths)

    for i in range(1, 6):
        for j in ["t001", "t003", "t005", "t007", "t009", "t011", "t013", "t015", "t017", "t019"]:
            dir = base_dir / "tree_height_benchmark" / f"iteration{i}" / j
            output_path = dir / "dataset.tgz"
            input_paths = [dir / "queries/", dir / "references/"]
            create_tar_archive(output_path, input_paths)