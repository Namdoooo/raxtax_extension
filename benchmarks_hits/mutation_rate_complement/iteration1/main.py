from pathlib import Path

import raxtax_extension_prototype.utils as utils
from simtools.config_handler import modify_config_at_path
from simtools.main_handler import create_main_at_path
from simtools.simulator import run_main_list

if __name__ == '__main__':
    leaf_count = 1000
    sequence_length = 50000
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

    mutation_seed = None
    disorientation_probability = 0.5
    disorientation_seed = None

    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    mutation_rate_list = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    main_dir_list = []

    for i in mutation_rate_list:
        mutation_rate = i
        config_dir = base_dir / ("m" + str(utils.float_to_string_without_point(mutation_rate)))
        config_dir.mkdir(parents=True, exist_ok=True)

        disorientation_seed = utils.create_random_seed()
        modify_config_at_path(base_dir=config_dir, redo_config=False, disorientation_probability=disorientation_probability,
                              disorientation_seed=disorientation_seed)

        main_dir = config_dir
        create_main_at_path(base_dir=main_dir, redo_main=False)
        main_dir_list.append(main_dir)

    #run_main_list(main_dir_list)

