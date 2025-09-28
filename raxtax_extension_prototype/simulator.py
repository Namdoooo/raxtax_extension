from pathlib import Path
import time
import yaml
import subprocess
import inspect

import raxtax_extension_prototype.data_generator as data_generator
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
    pass
