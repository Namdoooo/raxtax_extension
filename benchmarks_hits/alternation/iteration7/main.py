from pathlib import Path

import raxtax_extension_prototype.utils as utils
from simtools.config_handler import create_config_at_path
from simtools.main_handler import create_main_at_path
from simtools.simulator import run_main_list

if __name__ == '__main__':
    leaf_count = 1000
    sequence_length = 50000
    query_count = 200
    tree_height = 0.1
    core_count = 8
    query_min_length = 100
    fragment_count = 50
    nick_freq = 0.005
    overhang_parameter = 1.0
    double_strand_deamination = 0.0
    single_strand_deamination = 0.0
    iqtree_seed = utils.create_random_seed()
    pygargammel_seed = utils.create_random_seed()
    query_selection_seed = utils.create_random_seed()
    mutation_rate = -1
    mutation_seed = -1

    disorientation_seed = -1

    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    disorientation_probability_list = [-1, 0.5]
    main_dir_list = []

    for i in disorientation_probability_list:
        disorientation_probability = i
        if i == -1:
            config_dir = base_dir / "oriented"
        else:
            disorientation_seed = utils.create_random_seed()
            config_dir = base_dir / "disoriented"
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

