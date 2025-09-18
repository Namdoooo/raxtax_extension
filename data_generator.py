import subprocess
import yaml
from random import randint
from typing import Union

from pathlib import Path

from fasta_editor import phy_to_fasta
from fasta_editor import sample_fasta_every_x



def float_to_string_without_point(num: float) -> str:
    # Erst als String mit möglichst wenig Nachkommastellen darstellen
    s = format(num, 'f').rstrip('0').rstrip('.')
    return s.replace(".", "")

def create_folder(path: Union[Path, str]) -> None:

    folder_path = Path(path)
    folder_path.mkdir(parents=True, exist_ok=True)

    print(f"Ordner erstellt oder vorhanden: {folder_path.resolve()}")

def run_iqtree_simulation(path: Union[Path, str], leafcount: int, length: int, treeheight: float, seed_iqtree: int=None):
    # Pfad als Path-Objekt absichern
    alisim_path = Path(path)

    if not alisim_path.parent.exists():
        print(f"Pfad nicht gefunden: {alisim_path.parent}")
        return

    # Kommando zusammensetzen
    command = [
        "iqtree3",
        "--alisim", str(alisim_path),
        "--model", "GTR+G+I",
        "--tree", f"RANDOM{{yh/{leafcount}}}",
        "--length", str(length),
        "--branch-scale", str(treeheight),
    ]

    # Optional: Seed hinzufügen, wenn übergeben
    if seed_iqtree is not None:
        command += ["--seed", str(seed_iqtree)]

    print("Führe aus:", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)

    # Ausgabe anzeigen
    print("Ausgabe:")
    print(result.stdout)
    if result.stderr:
        print("Fehler:")
        print(result.stderr)

def run_pygargammel_simulation(path: Union[Path, str], seed_pygargammel: int=None, min_length: int=100, fragment_count: int=50,
                               nick_freq: float=0.005, overhang_parameter: float=1.0, double_strand_deamination: float=0.0, single_strand_deamination: float=0.0):
    home = Path.home()
    #pygargammel_path = home / "PycharmProjects" / "raxtax" / "pygargammel" / "pygargammel.py"
    pygargammel_path = home / "raxtax" / "pygargammel" / "pygargammel.py"


    data_path = Path(path)
    output_path = data_path.parent / "queries.fasta"

    pygargammel_log_path = data_path.parent / "pygargammel.log"

    command = [
        "python", str(pygargammel_path),
        "--fasta", str(data_path),
        "--nick-freq", str(nick_freq),
        "--overhang-parameter", str(overhang_parameter),
        "--double-strand-deamination", str(double_strand_deamination),
        "--single-strand-deamination", str(single_strand_deamination),
        "--output", str(output_path),
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

def simulate_references_queries(path_str: Union[Path, str], leafcount: int, length: int, treeheight: float, query_count: int, iqtree_seed: int=None, pygargammel_seed: int=None, query_selection_seed: int=None,
                                min_length: int=100, fragment_count: int=50):
    path = Path(path_str)
    print(f"Create referenes and queries at {path}, with leafcount={leafcount}, length={length}, treeheight={treeheight}")

    create_folder(path)

    alisim_path = Path(path) / f"references_s{leafcount}_t{float_to_string_without_point(treeheight)}"

    run_iqtree_simulation(alisim_path, leafcount, length, treeheight, iqtree_seed)

    phy_path = path / f"references_s{leafcount}_t{float_to_string_without_point(treeheight)}.phy"
    fasta_path = path / f"references.fasta"
    phy_to_fasta(phy_path, fasta_path)

    run_pygargammel_simulation(fasta_path, pygargammel_seed, min_length=min_length, fragment_count=fragment_count)

    query_path = path / f"queries.fasta"
    query_new_path = path / f"queries_{query_count}.fasta"
    x = (leafcount * fragment_count) // query_count

    sample_fasta_every_x(query_path, query_new_path, x, query_selection_seed)

def simulate_references_queries_with_config(config_path: Union[Path, str]):
    path = Path(config_path)

    # Load config.yaml
    with open(path, "r") as file:
        config = yaml.safe_load(file)

    leafcount = config["leaf_count"]
    length = config["sequence_length"]
    treeheight = config["tree_height"]
    query_count = config["query_count"]
    iqtree_seed = config.get("iqtree_seed", None)
    pygargammel_seed = config.get("pygargammel_seed", None)
    query_selection_seed = config.get("query_selection_seed", None)

    simulate_references_queries(path.parent, leafcount, length, treeheight, query_count, iqtree_seed, pygargammel_seed, query_selection_seed)

if __name__ == "__main__":
    seeds = []
    for i in range(10):
        seeds.append(randint(1, 1000))
    print(seeds)