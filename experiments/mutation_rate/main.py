from metadata_reader import marginalize_mutation_rate_results
from pathlib import Path

def visualize():
    root_dir = Path(__file__).resolve().parent
    folders = ["mutation_rate_boundary1", "mutation_rate_boundary2", "mutation_rate_boundary3", "mutation_rate_boundary4", "mutation_rate_boundary5"]
    marginalize_mutation_rate_results(root_dir, folders)

if __name__ == '__main__':
    visualize()