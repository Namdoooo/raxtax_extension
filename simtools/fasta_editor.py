import numpy as np
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import random
import os

import raxtax_extension_prototype.utils as utils

def phy_to_fasta(phy_path, fasta_path):
    with open(phy_path, 'r') as phy_file:
        lines = phy_file.readlines()

    # Read header line: num of sequences and sequence length
    header = lines[0].strip().split()
    num_sequences = int(header[0])

    fasta_lines = []

    # Read each sequence
    for line in lines[1:1 + num_sequences]:
        parts = line.strip().split()
        name = parts[0]
        sequence = ''.join(parts[1:])  # Handles cases where sequence is split by whitespace
        fasta_lines.append(f">{name}")
        fasta_lines.append(sequence)

    # Write to FASTA file
    with open(fasta_path, 'w') as fasta_file:
        fasta_file.write('\n'.join(fasta_lines))

    print(f"[INFO] Conversion complete. Saved as: {fasta_path}")

def reduce_fasta(input_path, output_path):
    anteil = 0.875

    # Read all records
    records = list(SeqIO.parse(input_path, "fasta"))

    # Take the first half
    split_index = int (len(records) * anteil)
    first_part = records[:split_index]

    # Write to new file
    SeqIO.write(first_part, output_path, "fasta")

    print(f"[INFO] Wrote {len(first_part)} sequences to {output_path}")

def complement_fasta(input_path, output_path):
    complement = str.maketrans("ACGTacgt", "TGCAtgca")

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                # Header-Zeile einfach übernehmen
                outfile.write(line)
            else:
                # Sequenzzeile komplementieren und schreiben
                comp_line = line.strip().translate(complement)
                outfile.write(comp_line + os.linesep)
    print(f"[INFO] Complemented sequences written to {output_path}")

def complement_alternate_fasta(input_path, output_path):
    complement = str.maketrans("ACGTacgt", "TGCAtgca")

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        entry_idx = -1
        for line in infile:
            if line.startswith(">"):
                # Neue Sequenz beginnt
                entry_idx += 1
                outfile.write(line)
            else:
                sequence = line.strip()
                if entry_idx % 2 == 1:
                    # Jeden zweiten Eintrag (1, 3, 5, ...) komplementieren
                    sequence = sequence.translate(complement)
                outfile.write(sequence + os.linesep)
    print(f"[INFO] Complemented alternate sequences written to {output_path}")

def complement_fasta_with_probability(input_path, output_path, p: float = 0.5, seed: int | None = None):
    complement = str.maketrans("ACGTacgt", "TGCAtgca")

    # Seed setzen
    if seed is None:
        seed = utils.create_random_seed()
        print(f"[INFO] Using randomly generated seed: {seed}")
    else:
        print(f"[INFO] Using provided seed: {seed}")
    random.seed(seed)

    records_out = []

    for record in SeqIO.parse(input_path, "fasta"):
        seq_str = str(record.seq)
        if random.random() < p:
            seq_str = seq_str.translate(complement)
        new_record = SeqRecord(Seq(seq_str), id=record.id, description=record.description)
        records_out.append(new_record)

    SeqIO.write(records_out, output_path, "fasta")

    print(f"[INFO] Sequences written to {output_path} with {p*100:.0f}% complement probability.")

    # Write log file
    log_path = output_path.with_suffix(output_path.suffix + ".log")
    with open(log_path, "w") as log_file:
        log_file.write("COMPLEMENT FASTA WITH PROBABILITY P LOG\n")
        log_file.write("==================\n")
        log_file.write(f"Input file     : {input_path}\n")
        log_file.write(f"Output file    : {output_path}\n")
        log_file.write(f"p  : {p}\n")
        log_file.write(f"Seed used      : {seed}\n")
        log_file.write(f"Sequences      : {len(records_out)}\n")

    print(f"[INFO] Log written to {log_path}")
    return seed

def disorient_fasta(input_path, output_path, p: float = 0.5, seed: int | None = None):
    return complement_fasta_with_probability(input_path, output_path, p=0.5, seed=seed)

def sample_fasta_every_x(input_path: str, output_path: str, x = 1, seed: int = None):

    # Seed setzen
    if seed is None:
        seed = utils.create_random_seed()
        print(f"[INFO] Using randomly generated seed: {seed}")
    else:
        print(f"[INFO] Using provided seed: {seed}")
    #rng = np.random.default_rng(seed)
    random.seed(seed)

    # Read all records
    records = list(SeqIO.parse(input_path, "fasta"))

    new_records = []

    for i in range(len(records) // x):
        #rnd_ind = rng.integers(0, x)
        rnd_ind = random.randint(0, x - 1)
        new_records.append(records[i * x + rnd_ind])

    SeqIO.write(new_records, output_path, "fasta")

    print(f"[INFO] Wrote {len(new_records)} sequences to {output_path}")

    # Write log file
    log_path = os.path.splitext(output_path)[0] + ".log"
    with open(log_path, "w") as log_file:
        log_file.write("FASTA EVERY X Log\n")
        log_file.write("==================\n")
        log_file.write(f"Input file     : {input_path}\n")
        log_file.write(f"Output file    : {output_path}\n")
        log_file.write(f"x  : {x}\n")
        log_file.write(f"Seed used      : {seed}\n")
        log_file.write(f"Sequences      : {len(new_records)}\n")

    print(f"[INFO] Log written to {log_path}")
    return seed

def mutate_fasta(input_path, output_path, mutation_rate, seed=None):
    bases = ["A", "C", "G", "T"]

    # Seed setzen
    if seed is None:
        seed = random.randint(0, 2**32 - 1)
        print(f"[INFO] Using randomly generated seed: {seed}")
    else:
        print(f"[INFO] Using provided seed: {seed}")
    random.seed(seed)


    def mutate_base(base):
        if base.upper() not in bases:
            return base  # N oder andere Buchstaben bleiben unverändert
        if random.random() < mutation_rate:
            other_bases = [b for b in bases if b != base.upper()]
            new_base = random.choice(other_bases)
            return new_base if base.isupper() else new_base.lower()
        else:
            return base

    sequence_count = 0

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                outfile.write(line)  # Header bleibt unverändert
                sequence_count += 1
            else:
                mutated_line = ''.join(mutate_base(base) for base in line.strip())
                outfile.write(mutated_line + "\n")

    print(f"{sequence_count} mutated sequences written to {output_path}")

    # Write log file
    log_path = os.path.splitext(output_path)[0] + ".log"
    with open(log_path, "w") as log_file:
        log_file.write("FASTA Mutation Log\n")
        log_file.write("==================\n")
        log_file.write(f"Input file     : {input_path}\n")
        log_file.write(f"Output file    : {output_path}\n")
        log_file.write(f"Mutation rate  : {mutation_rate}\n")
        log_file.write(f"Seed used      : {seed}\n")
        log_file.write(f"Sequences      : {sequence_count}\n")

    print(f"[INFO] Log written to {log_path}")
    return seed

if __name__ == "__main__":
    pass