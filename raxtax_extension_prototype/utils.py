import subprocess

import numpy as np
import re
from pathlib import Path
from typing import Union
import random
import raxtax_extension_prototype.constants as constants

def kmer_to_index(kmer: str) -> int:
    """
    Converts a k-mer string to an integer representation using a 2-bit encoding.
    """
    base_to_bits = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    index = 0
    for base in kmer:
        if base not in base_to_bits:
            return -1
        index = (index << 2) | base_to_bits[base]
    return index

def sequence_to_kmer_set(seq: str, k: int = 8) -> list[int]:
    """
    Converts a k-mer string to its set of k-mers in integer representation.
    """
    kmer_set = set()

    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k]
        index = kmer_to_index(kmer)
        if index != -1:
            kmer_set.add(index)

    return sorted(kmer_set)

def complement_sequence_str(sequence: str) -> str:
    """
    Computes the complementary sequence.
    """
    complement_table = str.maketrans("ACGTacgt", "TGCAtgca")
    return sequence.translate(complement_table)

def complement_kmer_index(kmer: int, k: int = constants.K):
    """
    Computes the integer representation of the complementary k-mer.
    """
    mask = (1 << (2 * k)) - 1
    return kmer ^ mask

def create_random_seed() -> int:
    """
    Generates a random 32-bit integer seed.
    """
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

def float_to_string_without_point(num: float) -> str:
    """
    Converts a floating-point number to a string without a decimal point.
    """
    s = format(num, 'f').rstrip('0').rstrip('.')
    return s.replace(".", "")

def create_folder(path: Union[Path, str]) -> None:
    """
    Creates a directory if it does not already exist.
    """

    folder_path = Path(path)
    folder_path.mkdir(parents=True, exist_ok=True)

    #print(f"[INFO] directory created or existed: {folder_path.resolve()}")

def generate_unique_numbers(n, count, seed=None):
    """
    Generates a sorted list of unique random integers from a given range.
    """
    if seed is not None:
        random.seed(seed)
    if count > n:
        raise ValueError("Count cannot be greater than the size of the range.")
    return sorted(random.sample(range(n), count))

def create_tar_archive(output_path: Path, input_paths:list[Path]) -> None:
    """
    Creates a compressed tar archive from the specified input paths and
    removes the original files or directories after archiving.
    """
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

    for i in range(1, 6):
        for j in [400, 800, 1200, 1600, 2000, 2400, 2800, 3200]:
            dir = base_dir / "reference_memory_benchmark_new" / f"iteration{i}" / f"leaf_count{j}"
            output_path = dir / "dataset.tgz"
            input_paths = [dir / "queries/", dir / "references/"]
            create_tar_archive(output_path, input_paths)


    for i in range(1, 6):
        for j in [100, 200, 300, 400, 500, 600, 800]:
            dir = base_dir / "query_memory_benchmark_new" / f"iteration{i}" / f"query_count{j}"
            output_path = dir / "dataset.tgz"
            input_paths = [dir / "queries/", dir / "references/"]
            create_tar_archive(output_path, input_paths)