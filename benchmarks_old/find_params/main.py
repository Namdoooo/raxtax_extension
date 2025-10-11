from pathlib import Path

from raxtax_extension_prototype.simulator import run_main_list

if __name__ == "__main__":
    main_dir_list = []

    for core_count in [8, 16]:
        for query_count in [500, 1000, 1500]:
            main_dir = Path(f"benchmarks_hits/find_params/core{core_count}/query{query_count}")
            main_dir_list.append(main_dir)

    run_main_list(main_dir_list)