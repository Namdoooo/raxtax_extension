"""
parser_short_long.py

Description
-----------
Module for matching short query sequences against long reference sequences.

The module provides functionality for reading and preprocessing reference
sequences, constructing lookup tables, loading and orienting query sequences
and computing k-mer intersection sizes between queries and references.
"""
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
    """
    Parses reference sequences from a FASTA file and
    constructs a k-mer lookup table.

    Parameters
    ----------
    reference_path : pathlib.Path
        Path to the reference FASTA file.
    result_path : pathlib.Path
        Path where the generated lookup table is stored in HDF5 format.
    redo : bool
        If False and the result file already exists, parsing is skipped.

    Returns
    -------
    None
        The function writes the lookup tables to disk.
    """
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

            kmer_map = [[] for _ in range(constants.KMER_COUNT)]

            for i in range(len(sequence) - constants.K + 1):
                kmer = utils.kmer_to_index(sequence[i:i + constants.K])
                kmer_map[kmer].append(i)
                kmer_occurrence_count[kmer] += 1

            #convert per-k-mer position lists into an offset-based flattened representation
            flat_data = np.concatenate(kmer_map)
            bucket_sizes = np.array([len(b) for b in kmer_map], dtype=np.uint32)
            offsets = np.concatenate((np.array([0]), np.cumsum(bucket_sizes)))

            grp = f.create_group(str(idx))
            grp.attrs["name"] = lineage
            grp.create_dataset("flat_data", data=flat_data, dtype=np.uint32, compression="gzip")
            grp.create_dataset("offsets", data=offsets, dtype=np.uint32, compression="gzip")

        f.create_dataset("kmer_occurrence_count", data=kmer_occurrence_count, dtype=np.uint32, compression="gzip")

def parse_query_fasta(query_path: Path):
    """
    Parses query sequences from a FASTA file and converts each query
    sequence into its k-mer set.

    Parameters
    ----------
    query_path : pathlib.Path
        Path to the query FASTA file.

    Returns
    -------
    dict
        Dictionary containing:
        - "query_names": list of query sequence identifiers
        - "kmer_sets": list of k-mer sets for each query sequence
        - "sequence_lengths": list of query sequence lengths
    """
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
    """
    Computes the maximum k-mer intersection size between a query and a
    sliding window within a reference sequence.

    Parameters
    ----------
    flat_data : numpy.ndarray
        Flattened array of k-mer positions for the reference sequence
        sorted lexicographically by k-mer identity.
    offsets : numpy.ndarray
        Offset array defining k-mer position ranges in flat_data.
    kmer_set : numpy.ndarray
        Query k-mer set.
    window_size : int
        Size of the sliding window applied to the reference sequence.

    Returns
    -------
    int
        Maximum k-mer intersection size between the query and the
        reference sequence.
    """
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
    """
    Computes k-mer intersection sizes sequentially between all query
    sequences and reference sequences.

    Parameters
    ----------
    reference_path : pathlib.Path
        Path to the reference FASTA file.
    query_path : pathlib.Path
        Path to the query FASTA file.
    orient_query : bool, optional
        If True, query sequences are oriented prior to matching.
    redo : bool, optional
        If True, existing reference lookup data are recomputed.

    Returns
    -------
    tuple
        A tuple containing:
        - result : list of tuples
            For each query, a tuple of the form
            (query_name, query_kmer_set_size, intersection_sizes),
            where intersection_sizes is a list of k-mer intersection
            sizes with all reference sequences.
        - reference_names : list of str
            Names of the reference sequences.
        - runtime_info : dict
            Dictionary containing runtime measurements for the
            individual processing steps.
    """

    #parse reference sequences
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

    #orient queries
    query_oriented_path = query_path
    orient_queries_time = 0
    if orient_query:
        orient_queries_start_time = time.perf_counter()
        query_oriented_path = query_path.with_name(query_path.stem + "_oriented" + query_path.suffix)
        orient_queries(query_path, result_path, redo=True)
        orient_queries_end_time = time.perf_counter()
        orient_queries_time = orient_queries_end_time - orient_queries_start_time

    #parse query sequences
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

    #calculate intersection sizes sequentially
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
    """
    Orients query sequences with respect to the reference database.

    Parameters
    ----------
    query_path : pathlib.Path
        Path to the query FASTA file.
    reference_data_path : pathlib.Path
        Path to the reference lookup table.
    redo : bool, optional
        If False and an oriented query file already exists, orientation
        is skipped.

    Returns
    -------
    None
        The oriented query sequences are written to disk.
    """
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
    """
    Computes k-mer intersection sizes between a single reference
    sequence and all query sequences.

    The function loads the k-mer lookup data of one reference sequence
    from disk and computes the k-mer intersection size between this
    reference and each query sequence. It is used when matching is
    parallelized across reference sequences.

    Parameters
    ----------
    idx : str
        Identifier of the reference sequence within the lookup table.
    result_path : pathlib.Path
        Path to the HDF5 file containing reference lookup data.
    query_kmer_sets : list of numpy.ndarray
        List of k-mer sets derived from the query sequences.
    query_sequence_lengths : list of int
        Lengths of the query sequences, used to define sliding window
        sizes.

    Returns
    -------
    tuple
        Tuple of the form (idx, lineage_name, intersection_sizes), where
        lineage name is the name of the reference sequence and
        intersection_sizes contains the k-mer intersection size between
        the reference sequence and each query.
    """
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
        #print(f"Processing {idx} reference took {reference_processing_time} seconds.")

    return idx, lineage_name, intersection_sizes

def get_intersection_sizes_parallel(reference_path: Path, query_path: Path, orient_query: bool = False, redo: bool = False, num_workers: int = None):
    """
    Computes k-mer intersection sizes between all query sequences
    and reference sequences using parallel processing.

    Parameters
    ----------
    reference_path : pathlib.Path
        Path to the reference FASTA file.
    query_path : pathlib.Path
        Path to the query FASTA file.
    orient_query : bool, optional
        If True, query sequences are oriented prior to matching.
    redo : bool, optional
        If True, existing reference lookup data are recomputed.
    num_workers : int, optional
        Number of parallel processes to use.

    Returns
    -------
    tuple
        A tuple containing:
        - result : list of tuples
            For each query, a tuple of the form
            (query_name, query_kmer_set_size, intersection_sizes),
            where intersection_sizes is a list of k-mer intersection
            sizes with all reference sequences.
        - reference_names : list of str
            Names of the reference sequences.
        - runtime_info : dict
            Dictionary containing runtime measurements for the
            individual processing steps.
    """

    #parse reference sequences
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

    #orient queries
    query_oriented_path = query_path
    orient_queries_time = 0
    if orient_query:
        orient_queries_start_time = time.perf_counter()
        query_oriented_path = query_path.with_name(query_path.stem + "_oriented" + query_path.suffix)
        orient_queries(query_path, result_path, redo=True)
        orient_queries_end_time = time.perf_counter()
        orient_queries_time = orient_queries_end_time - orient_queries_start_time

    #parse query sequences
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

    #calculate intersection sizes in parallel
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