from Bio import SeqIO

input_path = "./validator/example/diptera_queries.fasta"
output_path = "./validator/example/diptera_queries_complement_alternate.fasta"

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



complement_alternate_fasta(input_path, output_path)