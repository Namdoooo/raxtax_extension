from pathlib import Path
import yaml
import inspect

import raxtax_extension_prototype.utils as utils

def create_config_at_path(base_dir: Path, redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=0,
                          query_min_length: int=100, fragment_count: int=50, nick_freq: float=0.005, overhang_parameter: float=1.0, double_strand_deamination: float=0.0, single_strand_deamination: float=0.0):
    config_path = base_dir / "config.yaml"

    # Write config only if redo_config is True or file does not exist
    if redo_config or not config_path.exists():

        iqtree_seed = utils.create_random_seed()
        pygargammel_seed = utils.create_random_seed()
        query_selection_seed = utils.create_random_seed()

        config_data = {
            "leaf_count": leaf_count,
            "sequence_length": sequence_length,
            "tree_height": tree_height,
            "query_count": query_count,
            "query_min_length": query_min_length,
            "fragment_count": fragment_count,
            "nick_freq": nick_freq,
            "overhang_parameter": overhang_parameter,
            "double_strand_deamination": double_strand_deamination,
            "single_strand_deamination": single_strand_deamination,
            "core_count": core_count,
            "iqtree_seed": iqtree_seed,
            "pygargammel_seed": pygargammel_seed,
            "query_selection_seed": query_selection_seed,
        }

        with config_path.open("w") as f:
            yaml.dump(config_data, f, sort_keys=False)

        if not config_path.exists():
            print(f"[INFO] Created new configuration file at {config_path}")
        elif redo_config:
            print(f"[INFO] Re-created configuration file at {config_path}")

        print("    Parameters:")
        print("        leaf_count: " + str(leaf_count))
        print("        sequence_length: " + str(sequence_length))
        print("        tree_height: " + str(tree_height))
        print("        query_count: " + str(query_count))
        print("        query_min_length: " + str(query_min_length))
        print("        fragment_count: " + str(fragment_count))
        print("        nick_freq: " + str(nick_freq))
        print("        overhang_parameter: " + str(overhang_parameter))
        print("        double_strand_deamination: " + str(double_strand_deamination))
        print("        single_strand_deamination: " + str(single_strand_deamination))
        print("        core_count: " + str(core_count))
        print("        iqtree_seed: " + str(iqtree_seed))
        print("        pygargammel_seed: " + str(pygargammel_seed))
        print("        query_selection_seed: " + str(query_selection_seed))
    else:
        print(f"[INFO] Configuration file already exists at {config_path}, skipping creation")

    return config_path

def create_config_here(redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=0,
                       query_min_lenght: int=100, fragment_count: int=50, nick_freq: float=0.005, overhang_parameter: float=1.0, double_strand_deamination: float=0.0, single_strand_deamination: float=0.0):

    # Get the path of the file that called this function
    base_dir = Path(inspect.stack()[1].filename).resolve().parent

    return create_config_at_path(base_dir, redo_config, leaf_count, sequence_length, tree_height, query_count, core_count,
                                 query_min_lenght, fragment_count, nick_freq, overhang_parameter, double_strand_deamination, single_strand_deamination)
