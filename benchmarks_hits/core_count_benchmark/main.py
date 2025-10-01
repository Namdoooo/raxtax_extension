from pathlib import Path

from raxtax_extension_prototype.simulator import run_main_list

if __name__ == "__main__":
    main_list = []
    for i in [2, 3]:
        main_path = Path(f"benchmarks_hits/core_count_benchmark/iteration{i}")
        main_list.append(main_path)

    run_main_list(main_list)
