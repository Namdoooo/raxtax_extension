from Bio import SeqIO

input_path = "./validator/example/diptera_references.fasta"
output_path = "./validator/example/diptera_references_4.fasta"
anteil = 0.04

# Read all records
records = list(SeqIO.parse(input_path, "fasta"))

# Take the first half
split_index = int (len(records) * anteil)
first_part = records[:split_index]

# Write to new file
SeqIO.write(first_part, output_path, "fasta")

print(f"Wrote {len(first_part)} sequences to {output_path}")