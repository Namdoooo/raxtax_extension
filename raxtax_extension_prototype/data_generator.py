import subprocess
import yaml
import random

from pathlib import Path

import raxtax_extension_prototype.fasta_editor as fasta_editor
import raxtax_extension_prototype.utils as utils

def run_iqtree_simulation(reference_path: Path, leafcount: int, length: int, treeheight: float, seed_iqtree: int=None):
    print("[INFO] Create reference data.")

    if not reference_path.parent.exists():
        print(f"[ERROR] Path not found: {reference_path.parent}")
        return

    # Kommando zusammensetzen
    command = [
        "iqtree3",
        "--alisim", str(reference_path),
        "--model", "GTR+G+I",
        "--tree", f"RANDOM{{yh/{leafcount}}}",
        "--length", str(length),
        "--branch-scale", str(treeheight),
    ]

    # Optional: Seed hinzufügen, wenn übergeben
    if seed_iqtree is not None:
        command += ["--seed", str(seed_iqtree)]

    print("[INFO] Execute :", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)

    # Ausgabe anzeigen
    print("Ausgabe:")
    print(result.stdout)
    if result.stderr:
        print("Fehler:")
        print(result.stderr)

    print("[INFO] reference.phy data created.")

def run_pygargammel_simulation(queries_dir: Path, references_path: Path, seed_pygargammel: int=None, min_length: int=100, fragment_count: int=50,
                               nick_freq: float=0.005, overhang_parameter: float=1.0, double_strand_deamination: float=0.0, single_strand_deamination: float=0.0):

    pygargammel_path = Path(__file__).resolve().parent.parent / "pygargammel" / "pygargammel.py"

    queries_path = queries_dir / "queries.fasta"

    pygargammel_log_path = queries_dir / "pygargammel.log"

    command = [
        "python", str(pygargammel_path),
        "--fasta", str(references_path),
        "--nick-freq", str(nick_freq),
        "--overhang-parameter", str(overhang_parameter),
        "--double-strand-deamination", str(double_strand_deamination),
        "--single-strand-deamination", str(single_strand_deamination),
        "--output", str(queries_path),
        "--log", str(pygargammel_log_path),
        "--min-length", str(min_length),
        f"--max-fragments={fragment_count}",
        f"--min-fragments={fragment_count}"
    ]

    # Optional: Seed hinzufügen, wenn übergeben
    if seed_pygargammel is not None:
        command += ["--seed", str(seed_pygargammel)]

    print("Führe aus:", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)

    # Ausgabe anzeigen
    print("Ausgabe:")
    print(result.stdout)
    if result.stderr:
        print("Fehler:")
        print(result.stderr)

def simulate_references_queries(base_dir: Path, leafcount: int, length: int, treeheight: float, query_count: int, iqtree_seed: int=None, pygargammel_seed: int=None, query_selection_seed: int=None,
                                min_length: int=100, fragment_count: int=50, nick_freq: float=0.005, overhang_parameter: float=1.0, double_strand_deamination: float=0.0, single_strand_deamination: float=0.0):
    print(f"[INFO] Create references and queries at {base_dir}, with leafcount={leafcount}, length={length}, treeheight={treeheight}")


    reference_dir = base_dir / "references"
    utils.create_folder(reference_dir)

    reference_path = reference_dir / f"references_s{leafcount}_t{utils.float_to_string_without_point(treeheight)}"
    references_fasta_path = reference_dir / "references.fasta"

    if references_fasta_path.exists():
        print("[INFO] reference.fasta already exists, skipping creation.")
    else:
        run_iqtree_simulation(reference_path, leafcount, length, treeheight, iqtree_seed)

        reference_phy_path = reference_dir / f"references_s{leafcount}_t{utils.float_to_string_without_point(treeheight)}.phy"
        fasta_editor.phy_to_fasta(reference_phy_path, references_fasta_path)
        print("[INFO] reference.fasta created.")

    query_dir = base_dir / "queries"
    utils.create_folder(query_dir)
    query_path = query_dir / f"queries.fasta"

    if query_path.exists():
        print("[INFO] queries.fasta already exists, skipping creation.")
    else:
        run_pygargammel_simulation(query_dir, references_fasta_path, pygargammel_seed, min_length, fragment_count,
                                   nick_freq, overhang_parameter, double_strand_deamination, single_strand_deamination)

    query_new_path = query_dir / f"queries_{query_count}.fasta"
    x = (leafcount * fragment_count) // query_count

    if query_new_path.exists():
        print("[INFO] " + f"queries_{query_count}.fasta" + "already exists, skipping creation.")
    else:
        fasta_editor.sample_fasta_every_x(query_path, query_new_path, x, query_selection_seed)

def simulate_references_queries_with_config(config_path: Path, base_dir: Path):
    # Load config.yaml
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    leafcount = config["leaf_count"]
    length = config["sequence_length"]
    treeheight = config["tree_height"]
    query_count = config["query_count"]
    query_min_length = config["query_min_length"]
    fragment_count = config["fragment_count"]
    nick_freq = config["nick_freq"]
    overhang_parameter = config["overhang_parameter"]
    double_strand_deamination = config["double_strand_deamination"]
    single_strand_deamination = config["single_strand_deamination"]
    iqtree_seed = config.get("iqtree_seed", None)
    pygargammel_seed = config.get("pygargammel_seed", None)
    query_selection_seed = config.get("query_selection_seed", None)

    simulate_references_queries(base_dir, leafcount, length, treeheight, query_count, iqtree_seed, pygargammel_seed, query_selection_seed,
                                query_min_length, fragment_count, nick_freq, overhang_parameter, double_strand_deamination, single_strand_deamination)

if __name__ == "__main__":
    seeds = []
    for i in range(10):
        seeds.append(random.randint(1, 1000))
    print(seeds)