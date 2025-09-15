from Bio import SeqIO
import random

#input_path = "./validator/example/diptera_queries.fasta"
#output_path = "./validator/example/diptera_queries_complement_alternate.fasta"

input_path = "./example_short_long/s1000_t6/queries.fasta"
output_path = "./example_short_long/s1000_t6/queries_every_random_1000.fasta"

def reduce_fasta(input_path, output_path):
    anteil = 0.04

    # Read all records
    records = list(SeqIO.parse(input_path, "fasta"))

    # Take the first half
    split_index = int (len(records) * anteil)
    first_part = records[:split_index]

    # Write to new file
    SeqIO.write(first_part, output_path, "fasta")

    print(f"Wrote {len(first_part)} sequences to {output_path}")


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
                outfile.write(comp_line + "\n")
    print(f"Complemented sequences written to {output_path}")


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
                outfile.write(sequence + "\n")
    print(f"Complemented alternate sequences written to {output_path}")


def sample_fasta_every_x(input_path: str, output_path: str, x = 100):
    # Read all records
    records = list(SeqIO.parse(input_path, "fasta"))

    new_records = []

    for i in range(int(len(records) / x)):
        rnd_ind = random.randint(0, x - 1)
        if i == 0:
            rnd_ind = 0
        new_records.append(records[i * x + rnd_ind])

    SeqIO.write(new_records, output_path, "fasta")

    print(f"Wrote {len(new_records)} sequences to {output_path}")


if __name__ == "__main__":
    sample_fasta_every_x(input_path, output_path, 1000)