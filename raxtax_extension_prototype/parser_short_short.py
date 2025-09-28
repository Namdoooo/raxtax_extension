from Bio import SeqIO
from pathlib import Path
import pickle

from tree import Tree
import raxtax_extension_prototype.utils as utils

def parse_reference_fasta(reference_path: Path, result_path: Path, redo: bool = False):
    if result_path.exists() & (not redo):
        print("Lookup table already exists.")
        return

    print("Parsing reference sequences...")

    lineages = []
    sequences = []

    for record in SeqIO.parse(reference_path, "fasta"):
        parts = record.name.split(';tax=')
        lineages.append(parts[1])
        sequences.append(str(record.seq).upper())

    tree = Tree(lineages, sequences)

    with result_path.open("wb") as f:
        pickle.dump(tree, f)
        print("Lookup table saved!")

def load_reference_tree(reference_path: Path, redo: bool = False):
    result_path = reference_path.with_name(reference_path.stem + "_lookup.pkl")

    parse_reference_fasta(reference_path, result_path, redo)
    if not result_path.exists():
        raise ValueError("Lookup table does not exist.")

    with result_path.open("rb") as f:
        tree = pickle.load(f)

    print("Read look up table")

    return tree

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

def get_intersection_sizes(reference_path: Path, query_path: Path, redo: bool = False):

    reference_tree = load_reference_tree(reference_path, redo)
    query_data = parse_query_fasta(query_path)

    reference_names = reference_tree.lineages
    lookup_table = reference_tree.kmer_map

    query_names = query_data["query_names"]
    query_kmer_sets = query_data["kmer_sets"]

    result = []

    for i in range(len(query_kmer_sets)):

        intersection_sizes = [0 for _ in range(len(reference_names))]

        for kmer in query_kmer_sets[i]:
            for index in lookup_table[kmer]:
                intersection_sizes[index] += 1

        result.append((query_names[i], len(query_kmer_sets[i]), intersection_sizes))
        print(len(query_kmer_sets[i]))

    return result, reference_names