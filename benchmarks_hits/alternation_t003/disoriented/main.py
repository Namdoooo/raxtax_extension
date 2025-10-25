from pathlib import Path

import raxtax_extension_prototype.utils as utils
from simtools.config_handler import modify_config_at_path
from simtools.main_handler import create_main_at_path
from simtools.simulator import run_main_list

if __name__ == '__main__':
    disorientation_probability = 0.5
    disorientation_seed = -1

    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    iteration_list = range(1, 31)
    main_dir_list = []

    for i in iteration_list:
        config_dir = base_dir / f"iteration{i}"
        config_dir.mkdir(parents=True, exist_ok=True)

        disorientation_seed = utils.create_random_seed()
        modify_config_at_path(base_dir=config_dir, redo_config=False, disorientation_probability=disorientation_probability, disorientation_seed=disorientation_seed)


        main_dir = config_dir
        create_main_at_path(base_dir=main_dir, redo_main=False)
        main_dir_list.append(main_dir)

    #run_main_list(main_dir_list)

