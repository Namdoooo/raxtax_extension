def kmer_to_index(kmer: str) -> int:
    base_to_bits = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    index = 0
    for base in kmer:
        index = (index << 2) | base_to_bits[base]
    return index

def sequence_to_kmer_set(seq: str, k: int = 8) -> list[int]:
    kmer_set = set()

    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k]
        kmer_set.add(kmer_to_index(kmer))

    return sorted(kmer_set)