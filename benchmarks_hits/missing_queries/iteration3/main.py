from pathlib import Path

import yaml

import raxtax_extension_prototype.utils as utils
from simtools.config_handler import create_config_at_path
from simtools.config_handler import modify_config_at_path
from simtools.main_handler import create_specific_main_at_path
from simtools.data_generator import run_iqtree_simulation
import simtools.fasta_editor as fasta_editor
from simtools.simulator import run_main_list

if __name__ == '__main__':
    leaf_count = 1000
    sequence_length = -1
    query_count = 200
    tree_height = -1
    core_count = 8
    query_min_length = 100
    fragment_count = 50
    nick_freq = 0.005
    overhang_parameter = 1.0
    double_strand_deamination = 0.0
    single_strand_deamination = 0.0
    iqtree_seed = -1
    pygargammel_seed = utils.create_random_seed()
    query_selection_seed = utils.create_random_seed()
    mutation_rate = -1
    mutation_seed = -1
    disorientation_probability = -1
    disorientation_seed = -1
    missing_references_selection_seed = -1

    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent

    iteration_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    main_dir_list = []

    create_config_at_path(base_dir=base_dir, redo_config=False, leaf_count=1100, sequence_length=50000, tree_height=0.1, iqtree_seed=utils.create_random_seed())
    config_path = base_dir / "config.yaml"

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    all_leafcount = config["leaf_count"]
    all_length = config["sequence_length"]
    all_treeheight = config["tree_height"]
    all_iqtree_seed = config["iqtree_seed"]

    reference_dir = base_dir / "references"
    utils.create_folder(reference_dir)

    reference_path = reference_dir / f"references_s{all_leafcount}_t{utils.float_to_string_without_point(all_treeheight)}"
    references_fasta_path = reference_dir / "references.fasta"

    if references_fasta_path.exists():
        print("[INFO] reference.fasta already exists, skipping creation.")
    else:
        run_iqtree_simulation(reference_path, all_leafcount, all_length, all_treeheight, all_iqtree_seed)

        reference_phy_path = reference_dir / f"references_s{all_leafcount}_t{utils.float_to_string_without_point(all_treeheight)}.phy"
        fasta_editor.phy_to_fasta(reference_phy_path, references_fasta_path)
        print("[INFO] reference.fasta created.")

    for i in iteration_list:
        missing_references_selection_seed = utils.create_random_seed()

        config_dir = base_dir / f"iteration{i}"
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

        modify_config_at_path(base_dir=config_dir, redo_config=True, missing_references_selection_seed=missing_references_selection_seed)

        main_dir = config_dir
        create_specific_main_at_path(base_dir=main_dir, func_name="run_non_present_query_simulation", redo_main=False)
        main_dir_list.append(main_dir)

    #run_main_list(main_dir_list)

