from pathlib import Path

from simtools.config_handler import create_config_at_path
from simtools.main_handler import create_executable_at_path
from simtools.simulator import run_executable_dir_list

if __name__ == '__main__':
    leaf_count = 1200
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
    mutation_rate = -1
    mutation_seed = -1
    disorientation_probability = -1
    disorientation_seed = -1

    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    query_count_list = [100, 200, 300, 400, 500, 600, 800]

    executable_dir_list = []

    for i in query_count_list:
        query_count = i
        config_dir = base_dir / f"query_count{query_count}"
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

        executable_dir = config_dir
        create_executable_at_path(base_dir=executable_dir, func_name="generate_dateset", file_name="generate_dateset.py", redo_executable=False)
        create_executable_at_path(base_dir=executable_dir, func_name="calculate_lookup", file_name="calculate_lookup.py", redo_executable=False)
        create_executable_at_path(base_dir=executable_dir, func_name="execute_raxtax", file_name="execute_raxtax.py", redo_executable=False)

        executable_dir_list.append(executable_dir)

    #run_executable_dir_list(executable_dir_list)

