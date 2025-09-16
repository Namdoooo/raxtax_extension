from pathlib import Path
import time
import yaml
import subprocess
import inspect

from data_generator import simulate_references_queries_with_config
from parser_short_long import get_intersection_sizes_parallel
from parser_short_long import get_intersection_sizes
from output_adapters import output_s_t
from utils import create_random_seed

def create_config_at_path(base_dir: Path, redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=0):
    config_path = base_dir / "config.yaml"

    # Write config only if redo_config is True or file does not exist
    if redo_config or not config_path.exists():

        iqtree_seed = create_random_seed()
        pygargammel_seed = create_random_seed()
        query_selection_seed = create_random_seed()

        config_data = {
            "leaf_count": leaf_count,
            "sequence_length": sequence_length,
            "tree_height": tree_height,
            "query_count": query_count,
            "core_count": core_count,
            "iqtree_seed": iqtree_seed,
            "pygargammel_seed": pygargammel_seed,
            "query_selection_seed": query_selection_seed,
        }

        with config_path.open("w") as f:
            yaml.dump(config_data, f, sort_keys=False)

        print(f"Created configuration file: {config_path}")
    else:
        print(f"Configuration file already exists: {config_path}")

    return config_path

def create_config_here(redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=0):

    # Get the path of the file that called this function
    base_dir = Path(inspect.stack()[1].filename).resolve().parent

    return create_config_at_path(base_dir, redo_config, leaf_count, sequence_length, tree_height, query_count, core_count)

def run_simulation():
    base_dir = Path(inspect.stack()[1].filename).resolve().parent
    config_path = base_dir / "config.yaml"

    simulate_references_queries_with_config(config_path)

    # Load config.yaml
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    start_time = time.perf_counter()

    reference_path = base_dir / "references.fasta"
    query_path = base_dir / f"queries_{config['query_count']}.fasta"

    core_count = config.get("core_count", 0)

    if core_count == 0:
        results, names, runtime_info = get_intersection_sizes(reference_path, query_path, True)
    else:
        results, names, runtime_info = get_intersection_sizes_parallel(reference_path, query_path, True, config["core_count"])

    ref_name = reference_path.stem
    query_name = query_path.stem
    output_dir_name = f"results_{ref_name}_{query_name}"

    result_dir = base_dir / output_dir_name

    end_time = time.perf_counter()
    total_execution_time = end_time - start_time
    output_s_t(results, names, runtime_info, result_dir, total_execution_time)

def run_all_main():
    base_dir = Path(inspect.stack()[1].filename).resolve().parent
    print(base_dir)

    # Suche alle main.py-Dateien in direkten Unterordnern
    for subdir in base_dir.iterdir():
        print(subdir)
        script_path = subdir / "main.py"
        if script_path.is_file():
            print(f"Running {script_path}...")
            subprocess.run(["python", str(script_path)], check=True)

if __name__ == "__main__":
    path = Path("experiments/random_testing/single_vs_quadruple_core/single/single5")
    create_config_at_path(path, redo_config=True)
