from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import h5py
import time
import numpy as np
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

import raxtax_extension_prototype.constants as constants
import raxtax_extension_prototype.utils as utils

def parse_reference_fasta(reference_path: Path, result_path: Path, redo: bool):

    if result_path.exists() and not redo:
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

        kmer_occurrence_count = np.zeros(constants.KMER_COUNT, dtype=np.uint32)

        for idx, (lineage, sequence) in enumerate(lin_seq_pair):
            #print(idx)
            #print(lineage)
            #print(sequence)

            kmer_map = [[] for _ in range(constants.KMER_COUNT)]

            for i in range(len(sequence) - constants.K + 1):
                kmer = utils.kmer_to_index(sequence[i:i + constants.K])
                kmer_map[kmer].append(i)
                kmer_occurrence_count[kmer] += 1

            flat_data = np.concatenate(kmer_map)
            bucket_sizes = np.array([len(b) for b in kmer_map], dtype=np.uint32)
            offsets = np.concatenate((np.array([0]), np.cumsum(bucket_sizes)))

            grp = f.create_group(str(idx))
            grp.attrs["name"] = lineage
            grp.create_dataset("flat_data", data=flat_data, dtype=np.uint32, compression="gzip")
            grp.create_dataset("offsets", data=offsets, dtype=np.uint32, compression="gzip")

        f.create_dataset("kmer_occurrence_count", data=kmer_occurrence_count, dtype=np.uint32, compression="gzip")

def parse_query_fasta(query_path: Path):
    query_names = []
    kmer_sets = []
    sequence_lengths = []

    for record in SeqIO.parse(query_path, "fasta"):
        query_names.append(record.name)
        seq = str(record.seq).upper()

        kmer_sets.append(utils.sequence_to_kmer_set(seq))
        sequence_lengths.append(len(seq))

    data = {
        "query_names": query_names,
        "kmer_sets": kmer_sets,
        "sequence_lengths": sequence_lengths,
    }

    return data

def calculate_intersection_size(flat_data: np.ndarray, offsets: np.ndarray, kmer_set: np.ndarray, window_size: int):
    max_intersection_size = 0

    window_intersection_sizes = {}

    for kmer in kmer_set:
        pre_index = -1
        for index in flat_data[offsets[kmer]:offsets[kmer + 1]]:
            index = int(index)
            for i in range(max(pre_index + 1, index - window_size + constants.K), index + 1):
                if i in window_intersection_sizes:
                    window_intersection_sizes[i] += 1
                else:
                    window_intersection_sizes[i] = 1
                max_intersection_size = max(max_intersection_size, window_intersection_sizes[i])
            pre_index = index

    return max_intersection_size

def get_intersection_sizes(reference_path: Path, query_path: Path, orient_query: bool = False, redo: bool = False):
    result_path = reference_path.with_name(reference_path.stem + "_data.h5")

    reference_start_time = time.perf_counter()
    parse_reference_fasta(reference_path, result_path, redo)
    reference_end_time = time.perf_counter()
    reference_parse_time = reference_end_time - reference_start_time
    if reference_parse_time < 1:
        reference_parse_time = -1
        print("Lookup table already exists.")
    else:
        print("Lookup table created.")
        print(f"Parsing and storing reference look up took {reference_parse_time} seconds.")

    query_oriented_path = query_path
    orient_queries_time = 0
    if orient_query:
        orient_queries_start_time = time.perf_counter()
        query_oriented_path = query_path.with_name(query_path.stem + "_oriented" + query_path.suffix)
        orient_queries(query_path, result_path, redo=True)
        orient_queries_end_time = time.perf_counter()
        orient_queries_time = orient_queries_end_time - orient_queries_start_time


    query_start_time = time.perf_counter()
    query_data = parse_query_fasta(query_oriented_path)
    query_end_time = time.perf_counter()
    query_parse_time = query_end_time - query_start_time
    print(f"Parsing query sequences took {query_parse_time} seconds.")


    query_names = query_data["query_names"]
    query_kmer_sets = query_data["kmer_sets"]
    query_sequence_lengths = query_data["sequence_lengths"]

    intersection_sizes = [[] for _ in range(len(query_names))]
    reference_names = []

    calculate_intersection_sizes_start = time.perf_counter()
    average_reference_processing_time = 0
    with h5py.File(result_path, "r") as f:
        for idx in f.keys():
            reference_processing_time_start = time.perf_counter()
            grp = f[idx]
            lineage_name = grp.attrs["name"]
            print(idx, lineage_name)
            flat_data = grp["flat_data"][:]
            offsets = grp["offsets"][:]

            reference_names.append(lineage_name)

            for query_id, kmer_set in enumerate(query_kmer_sets):
                intersection_sizes[query_id].append(calculate_intersection_size(flat_data, offsets, kmer_set, query_sequence_lengths[query_id]))

            reference_processing_time_end = time.perf_counter()
            reference_processing_time = reference_processing_time_end - reference_processing_time_start
            print(f"Processing {idx} reference took {reference_processing_time} seconds.")
            average_reference_processing_time += reference_processing_time
        average_reference_processing_time /= len(f.keys())
    calculate_intersection_sizes_end = time.perf_counter()
    calculate_intersection_sizes_time = calculate_intersection_sizes_end - calculate_intersection_sizes_start
    print(f"Calculating intersection sizes took {calculate_intersection_sizes_time} seconds.")

    result = []

    for query_id in range(len(query_names)):
        result.append((query_names[query_id], len(query_kmer_sets[query_id]), intersection_sizes[query_id]))

    runtime_info = {
        "reference_parse_time": reference_parse_time,
        "query_parse_time": query_parse_time,
        "orient_queries_time": orient_queries_time,
        "calculate_intersection_sizes_time": calculate_intersection_sizes_time,
        "average_reference_processing_time": average_reference_processing_time,
    }

    return result, reference_names, runtime_info

def orient_queries(query_path: Path, reference_data_path: Path, redo: bool = False):
    print(f"[INFO] Orient queries from: {query_path}")
    oriented_path = query_path.with_name(query_path.stem + "_oriented" + query_path.suffix)

    if not redo and oriented_path.exists():
        print(f"[INFO] Queries already oriented, skipping orienting queries.")
        return

    with h5py.File(reference_data_path, "r") as f:
        kmer_occurrence_count = f["kmer_occurrence_count"][:]

    records_out = []

    for record in SeqIO.parse(query_path, "fasta"):
        kmer_net_count = 0
        seq_str = str(record.seq)

        for kmer_int in utils.sequence_to_kmer_set(seq_str, constants.K):
            kmer_complement_int = utils.complement_kmer_index(kmer_int)
            kmer_net_count += int(kmer_occurrence_count[kmer_int])
            kmer_net_count -= int(kmer_occurrence_count[kmer_complement_int])

        if kmer_net_count >= 0:
            records_out.append(record)
        else:
            new_record = SeqRecord(Seq(utils.complement_sequence_str(seq_str)), id=record.id, description=record.description)
            records_out.append(new_record)

    SeqIO.write(records_out, oriented_path, "fasta")
    print(f"[INFO] Oriented queries written to: {oriented_path}")

def process_reference(idx, result_path, query_kmer_sets, query_sequence_lengths):
    with h5py.File(result_path, "r") as f:
        reference_processing_time_start = time.perf_counter()
        grp = f[idx]
        lineage_name = grp.attrs["name"]
        flat_data = grp["flat_data"][:]
        offsets = grp["offsets"][:]

        intersection_sizes = []
        for query_id, kmer_set in enumerate(query_kmer_sets):
            size = calculate_intersection_size(flat_data, offsets, kmer_set, query_sequence_lengths[query_id])
            intersection_sizes.append(size)

        reference_processing_time_end = time.perf_counter()
        reference_processing_time = reference_processing_time_end - reference_processing_time_start
        print(f"Processing {idx} reference took {reference_processing_time} seconds.")

    return idx, lineage_name, intersection_sizes

def get_intersection_sizes_parallel(reference_path: Path, query_path: Path, orient_query: bool = False, redo: bool = False, num_workers: int = None):
    result_path = reference_path.with_name(reference_path.stem + "_data.h5")

    reference_start_time = time.perf_counter()
    parse_reference_fasta(reference_path, result_path, redo)
    reference_end_time = time.perf_counter()
    reference_parse_time = reference_end_time - reference_start_time
    if reference_parse_time < 1:
        reference_parse_time = -1
        print("Lookup table already exists.")
    else:
        print("Lookup table created.")
        print(f"Parsing and storing reference look up took {reference_parse_time} seconds.")

    query_oriented_path = query_path
    orient_queries_time = 0
    if orient_query:
        orient_queries_start_time = time.perf_counter()
        query_oriented_path = query_path.with_name(query_path.stem + "_oriented" + query_path.suffix)
        orient_queries(query_path, result_path, redo=True)
        orient_queries_end_time = time.perf_counter()
        orient_queries_time = orient_queries_end_time - orient_queries_start_time

    query_start_time = time.perf_counter()
    query_data = parse_query_fasta(query_oriented_path)
    query_end_time = time.perf_counter()
    query_parse_time = query_end_time - query_start_time
    print(f"Parsing query sequences took {query_parse_time} seconds.")


    query_names = query_data["query_names"]
    query_kmer_sets = query_data["kmer_sets"]
    query_sequence_lengths = query_data["sequence_lengths"]

    intersection_sizes = [[] for _ in range(len(query_names))]
    reference_names = []

    calculate_intersection_sizes_start = time.perf_counter()
    reference_count = -1

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        with h5py.File(result_path, "r") as f:
            reference_count = len(f.keys())
            for idx in f.keys():
                if idx != "kmer_occurrence_count":
                    futures.append(executor.submit(
                        process_reference, idx, result_path, query_kmer_sets, query_sequence_lengths
                    ))

        for future in futures:
            idx, lineage_name, sizes = future.result()
            reference_names.append(lineage_name)
            for query_id, size in enumerate(sizes):
                intersection_sizes[query_id].append(size)

    calculate_intersection_sizes_end = time.perf_counter()
    calculate_intersection_sizes_time = calculate_intersection_sizes_end - calculate_intersection_sizes_start
    average_reference_processing_time = calculate_intersection_sizes_time / reference_count
    print(f"Calculating intersection sizes took {calculate_intersection_sizes_time} seconds.")

    result = []

    for query_id in range(len(query_names)):
        result.append((query_names[query_id], len(query_kmer_sets[query_id]), intersection_sizes[query_id]))

    runtime_info = {
        "reference_parse_time": reference_parse_time,
        "query_parse_time": query_parse_time,
        "orient_queries_time": orient_queries_time,
        "calculate_intersection_sizes_time": calculate_intersection_sizes_time,
        "average_reference_processing_time": average_reference_processing_time,
    }

    return result, reference_names, runtime_info