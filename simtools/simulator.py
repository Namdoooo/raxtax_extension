from pathlib import Path
import time
import yaml
import subprocess
import inspect

import simtools.data_generator as data_generator
import simtools.fasta_editor as fasta_editor
import raxtax_extension_prototype.parser_short_long as parser
import raxtax_extension_prototype.output_adapters as output_adapters


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

    mutation_rate = config.get("mutation_rate", -1)
    mutation_seed = config.get("mutation_seed", -1)
    disorientation_probability = config.get("disorientation_probability", -1)
    disorientation_seed = config.get("disorientation_seed", -1)

    if mutation_seed != -1:
        query_mutated_path = query_path.with_name(query_path.stem + "_mutated" + query_path.suffix)
        fasta_editor.mutate_fasta(query_path, query_mutated_path, mutation_rate, seed=mutation_seed)
        query_path = query_mutated_path

    orient_query_bool = False
    if disorientation_seed != -1:
        query_disoriented_path = query_path.with_name(query_path.stem + "_disoriented" + query_path.suffix)
        fasta_editor.disorient_fasta(query_path, query_disoriented_path, p=disorientation_probability, seed=disorientation_seed)
        query_path = query_disoriented_path
        orient_query_bool = True

    if core_count == 0:
        results, names, runtime_info = parser.get_intersection_sizes(reference_path, query_path, orient_query=orient_query_bool,redo=True)
    else:
        results, names, runtime_info = parser.get_intersection_sizes_parallel(reference_path, query_path, redo=True, orient_query=orient_query_bool, num_workers=core_count)

    ref_name = reference_path.stem
    query_name = query_path.stem
    output_dir_name = f"results_{ref_name}_{query_name}"

    result_dir = base_dir / output_dir_name

    end_time = time.perf_counter()
    total_execution_time = end_time - start_time
    output_adapters.output_s_t(results, names, runtime_info, result_dir, total_execution_time)

def run_non_present_query_simulation(config_dir: Path | None = None) :
    base_dir = Path(inspect.stack()[1].filename).resolve().parent
    if config_dir is None:
        config_dir = base_dir
    config_path = config_dir / "config.yaml"

    all_references_path = base_dir.parent / "references" / "references.fasta"
    data_generator.simulate_references_missing_queries_with_config(config_path, base_dir, all_references_path)

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    start_time = time.perf_counter()

    reference_path = base_dir / "references" / "present_references.fasta"
    query_path = base_dir / "queries" / f"queries_{config['query_count']}.fasta"

    core_count = config.get("core_count", 0)

    if core_count == 0:
        results, names, runtime_info = parser.get_intersection_sizes(reference_path, query_path, redo=True)
    else:
        results, names, runtime_info = parser.get_intersection_sizes_parallel(reference_path, query_path, redo=True, num_workers=core_count)

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

def run_main_list(main_dir_list: list[Path]):
    for main_dir in main_dir_list:
        main_path = main_dir / "main.py"
        print(main_path)
        print(main_path.is_file())
        if main_path.is_file():
            rel_parts = main_path.with_suffix("").parts
            if "raxtax" in rel_parts:
                rel_parts = rel_parts[rel_parts.index("raxtax") + 1 :]
            module_path = ".".join(rel_parts)
            print(f"Running {module_path}...")
            subprocess.run(["python", "-m", module_path], check=True)

if __name__ == "__main__":
    pass
