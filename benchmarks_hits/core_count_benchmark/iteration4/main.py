from pathlib import Path

import raxtax_extension_prototype.utils as utils
from raxtax_extension_prototype.config_handler import create_config_at_path
from raxtax_extension_prototype.main_handler import create_main_at_path
from raxtax_extension_prototype.simulator import run_main_list

if __name__ == '__main__':
    leaf_count = 1000
    sequence_length = 50000
    tree_height = 0.1
    query_count = 200
    query_min_length = 100
    fragment_count = 50
    nick_freq = 0.005
    overhang_parameter = 1.0
    double_strand_deamination = 0.0
    single_strand_deamination = 0.0
    iqtree_seed = utils.create_random_seed()
    pygargammel_seed = utils.create_random_seed()
    query_selection_seed = utils.create_random_seed()

    base_dir = Path(f"benchmarks_hits/core_count_benchmark/iteration4")

    for i in (0, 1, 2, 4, 8, 16, 24, 32, 40, 48):
        core_count = i
        config_dir = base_dir / f"core{i}"
        config_dir.mkdir(parents=True, exist_ok=True)

        create_config_at_path(base_dir=config_dir,
                              redo_config=False,
                              leaf_count=leaf_count,
                              sequence_length=sequence_length,
                              tree_height=tree_height,
                              query_count=query_count,
                              core_count=core_count,
                              query_min_length=query_min_length,
                              fragment_count=fragment_count,
                              nick_freq=nick_freq,
                              overhang_parameter=overhang_parameter,
                              double_strand_deamination=double_strand_deamination,
                              single_strand_deamination=single_strand_deamination,
                              iqtree_seed=iqtree_seed,
                              pygargammel_seed=pygargammel_seed,
                              query_selection_seed=query_selection_seed)

        main_dir = config_dir
        create_main_at_path(base_dir=main_dir, redo_main=False)


    main_dir_list = []
    for i in (0, 1, 2, 4, 8, 16, 24, 32, 40, 48):
        main_dir = base_dir / f"core{i}"
        main_dir_list.append(main_dir)

    #run_main_list(main_dir_list)

