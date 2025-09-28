from pathlib import Path
import time
import yaml
import subprocess
import inspect

import raxtax_extension_prototype.data_generator as data_generator
import raxtax_extension_prototype.parser_short_long as parser
import raxtax_extension_prototype.output_adapters as output_adapters
import raxtax_extension_prototype.utils as utils

def create_config_at_path(base_dir: Path, redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=0):
    config_path = base_dir / "config.yaml"

    # Write config only if redo_config is True or file does not exist
    if redo_config or not config_path.exists():

        iqtree_seed = utils.create_random_seed()
        pygargammel_seed = utils.create_random_seed()
        query_selection_seed = utils.create_random_seed()

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

        if not config_path.exists():
            print(f"[INFO] Created new configuration file at {config_path}")
        elif redo_config:
            print(f"[INFO] Re-created configuration file at {config_path}")

        print("    Parameters:")
        print("        base_dir: " + str(base_dir))
        print("        redo config: " + str(redo_config))
        print("        leaf_count: " + str(leaf_count))
        print("        sequence_length: " + str(sequence_length))
        print("        tree_height: " + str(tree_height))
        print("        query_count: " + str(query_count))
        print("        core_count: " + str(core_count))
    else:
        print(f"[INFO] Configuration file already exists at {config_path}, skipping creation")

    return config_path

def create_config_here(redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=0):

    # Get the path of the file that called this function
    base_dir = Path(inspect.stack()[1].filename).resolve().parent

    return create_config_at_path(base_dir, redo_config, leaf_count, sequence_length, tree_height, query_count, core_count)

def run_simulation(config_dir: Path | None = None):
    base_dir = Path(inspect.stack()[1].filename).resolve().parent
    if config_dir is None:
        config_dir = base_dir
    config_path = config_dir / "config.yaml"

    data_generator.simulate_references_queries_with_config(config_path, base_dir)

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    start_time = time.perf_counter()

    reference_path = base_dir / "references" / "references.fasta"
    query_path = base_dir / "queries" / f"queries_{config['query_count']}.fasta"

    core_count = config.get("core_count", 0)

    if core_count == 0:
        results, names, runtime_info = parser.get_intersection_sizes(reference_path, query_path, True)
    else:
        results, names, runtime_info = parser.get_intersection_sizes_parallel(reference_path, query_path, True, config["core_count"])

    ref_name = reference_path.stem
    query_name = query_path.stem
    output_dir_name = f"results_{ref_name}_{query_name}"

    result_dir = base_dir / output_dir_name

    end_time = time.perf_counter()
    total_execution_time = end_time - start_time
    output_adapters.output_s_t(results, names, runtime_info, result_dir, total_execution_time)

def run_all_main():
    base_dir = Path(inspect.stack()[1].filename).resolve().parent
    print(base_dir)

    # Suche alle main.py-Dateien in direkten Unterordnern
    for subdir in base_dir.iterdir():
        print(subdir)
        script_path = subdir / "main.py"
        if script_path.is_file():
            rel_parts = script_path.with_suffix("").parts
            if "raxtax" in rel_parts:
                rel_parts = rel_parts[rel_parts.index("raxtax") + 1 :]
            module_path = ".".join(rel_parts)
            print(f"Running {module_path}...")
            subprocess.run(["python", "-m", module_path], check=True)

if __name__ == "__main__":
    for i in range(3, 9):
        path = Path("../experiments/random_testing/core_count_benchmark1/core" + str(i))
        print(path)
        create_config_at_path(path, redo_config=False, core_count=i)
