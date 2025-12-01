from pathlib import Path

from simtools.simulator import run_main_list

if __name__ == "__main__":
    main_list = []
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    query_memory_benchmark_new_dir = base_dir / "query_memory_benchmark_new" / "iteration1"
    reference_memory_benchmark_new_dir = base_dir / "reference_memory_benchmark_new" / "iteration1"
    main_list.append(query_memory_benchmark_new_dir)
    main_list.append(reference_memory_benchmark_new_dir)

    run_main_list(main_list)
