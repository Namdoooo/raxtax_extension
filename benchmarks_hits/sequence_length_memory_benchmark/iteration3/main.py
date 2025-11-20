from pathlib import Path

from simtools.config_handler import create_config_at_path
from simtools.main_handler import create_main_at_path
from simtools.simulator import run_main_list

if __name__ == '__main__':
    leaf_count = 1000

    tree_height = 0.1
    query_count = 200
    core_count = 8
    query_min_length = 100
    fragment_count = 50
    nick_freq = 0.005
    overhang_parameter = 1.0
    double_strand_deamination = 0.0
    single_strand_deamination = 0.0
    iqtree_seed = None
    pygargammel_seed = None
    query_selection_seed = None
    mutation_rate = -1
    mutation_seed = -1
    disorientation_probability = -1
    disorientation_seed = -1

    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    sequence_length_list = [20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000]

    main_dir_list = []

    for i in sequence_length_list:
        sequence_length = i
        config_dir = base_dir / f"sequence_length{sequence_length}"
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
                              query_selection_seed=query_selection_seed,
                              mutation_rate=mutation_rate,
                              mutation_seed=mutation_seed,
                              disorientation_probability=disorientation_probability,
                              disorientation_seed=disorientation_seed)

        main_dir = config_dir
        create_main_at_path(base_dir=main_dir, redo_main=False)
        main_dir_list.append(main_dir)

    #run_main_list(main_dir_list)

