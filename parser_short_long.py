from Bio import SeqIO
from pathlib import Path
import numpy as np
import pickle
import h5py
import time

from constants import *
from utils import *

def parse_reference_fasta(reference_path: Path, result_path: Path):
    start = time.perf_counter()

    if result_path.exists():
        print("Lookup table already exists.")
        return

    print("Parsing reference sequences...")

    lineages = []
    sequences = []

    for record in SeqIO.parse(reference_path, "fasta"):
        parts = record.name.split(';tax=')
        if len(parts) > 1:
            lineages.append(parts[1])
        else:
            lineages.append(parts[0])
        seq = str(record.seq).upper()
        sequences.append(seq)

    print(f"{len(lineages)} lineages found.")

    lin_seq_pair = zip(lineages, sequences)

    with h5py.File(result_path, "w", track_order=True) as f:

        for idx, (lineage, sequence) in enumerate(lin_seq_pair):
            print(idx)
            print(lineage)
            print(sequence)

            kmer_map = [[] for _ in range(KMER_COUNT)]

            for i in range(len(sequence) - K + 1):
                kmer = kmer_to_index(sequence[i:i + K])
                kmer_map[kmer].append(i)

            flat_data = np.concatenate(kmer_map)
            bucket_sizes = np.array([len(b) for b in kmer_map], dtype=np.uint32)
            offsets = np.concatenate((np.array([0]), np.cumsum(bucket_sizes)))

            grp = f.create_group(str(idx))
            grp.attrs["name"] = lineage
            grp.create_dataset("flat_data", data=flat_data, dtype=np.uint32, compression="gzip")
            grp.create_dataset("offsets", data=offsets, dtype=np.uint32, compression="gzip")

    print("Lookup table created.")

    end = time.perf_counter()
    print(f"Parsing and storing reference look up took {end - start} seconds.")

def parse_query_fasta(query_path: Path):
    start = time.perf_counter()

    query_names = []
    kmer_sets = []
    sequence_lengths = []

    for record in SeqIO.parse(query_path, "fasta"):
        query_names.append(record.name)
        seq = str(record.seq).upper()

        kmer_sets.append(sequence_to_kmer_set(seq))
        sequence_lengths.append(len(seq))

    data = {
        "query_names": query_names,
        "kmer_sets": kmer_sets,
        "sequence_lengths": sequence_lengths,
    }

    end = time.perf_counter()
    print(f"Parsing query sequences took {end - start} seconds.")

    return data

def calculate_intersection_size(flat_data: np.ndarray, offsets: np.ndarray, kmer_set: np.ndarray, window_size: int):
    max_intersection_size = 0

    window_intersection_sizes = {}

    for kmer in kmer_set:
        pre_index = -1
        for index in flat_data[offsets[kmer]:offsets[kmer + 1]]:
            index = int(index)
            for i in range(max(pre_index + 1, index - window_size + K), index + 1):
                if i in window_intersection_sizes:
                    window_intersection_sizes[i] += 1
                else:
                    window_intersection_sizes[i] = 1
                max_intersection_size = max(max_intersection_size, window_intersection_sizes[i])
            pre_index = index

    return max_intersection_size

def get_intersection_sizes(reference_path: Path, query_path: Path):
    result_path = reference_path.with_name(reference_path.stem + "_data.h5")

    parse_reference_fasta(reference_path, result_path)

    query_data = parse_query_fasta(query_path)

    query_names = query_data["query_names"]
    query_kmer_sets = query_data["kmer_sets"]
    query_sequence_lengths = query_data["sequence_lengths"]

    intersection_sizes = [[] for _ in range(len(query_names))]
    reference_names = []

    with h5py.File(result_path, "r") as f:
        for idx in f.keys():
            start = time.perf_counter()
            grp = f[idx]
            lineage_name = grp.attrs["name"]
            flat_data = grp["flat_data"][:]
            offsets = grp["offsets"][:]

            reference_names.append(lineage_name)

            for query_id, kmer_set in enumerate(query_kmer_sets):
                intersection_sizes[query_id].append(calculate_intersection_size(flat_data, offsets, kmer_set, query_sequence_lengths[query_id]))

            end = time.perf_counter()
            print(f"Processing {idx} reference took {end - start} seconds.")

    result = []

    for query_id in range(len(query_names)):
        result.append((query_names[query_id], len(query_kmer_sets[query_id]), intersection_sizes[query_id]))

    return result, reference_names