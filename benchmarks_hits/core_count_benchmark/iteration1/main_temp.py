from pathlib import Path
from raxtax_extension_prototype.simulator import run_main_list

if __name__ == "__main__":
    main_list = []
    for i in [16, 24, 32, 40, 48]:
        main_path = Path("benchmarks_hits/core_count_benchmark/iteration1/core" + str(i))
        main_list.append(main_path)

    run_main_list(main_list)