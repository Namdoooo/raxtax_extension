from pathlib import Path
import yaml
import inspect

import raxtax_extension_prototype.utils as utils

def create_config_at_path(base_dir: Path, redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=8,
                          query_min_length: int=100, fragment_count: int=50, nick_freq: float=0.005, overhang_parameter: float=1.0, double_strand_deamination: float=0.0, single_strand_deamination: float=0.0,
                          iqtree_seed: int | None = None, pygargammel_seed: int | None = None, query_selection_seed: int | None=None,
                          mutation_rate: float | None = None, mutation_seed: int | None = None, disorientation_probability: float | None = None, disorientation_seed: int | None = None):
    config_path = base_dir / "config.yaml"

    # Write config only if redo_config is True or file does not exist
    if redo_config or not config_path.exists():

        if iqtree_seed is None:
            iqtree_seed = utils.create_random_seed()
        if pygargammel_seed is None:
            pygargammel_seed = utils.create_random_seed()
        if query_selection_seed is None:
            query_selection_seed = utils.create_random_seed()

        if mutation_rate is None:
            mutation_rate = -1
            mutation_seed = -1
        else:
            if mutation_seed is None:
                mutation_seed = utils.create_random_seed()

        if disorientation_probability is None:
            disorientation_probability = -1
            disorientation_seed = -1
        else:
            if disorientation_seed is None:
                disorientation_seed = utils.create_random_seed()

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
            "mutation_rate": mutation_rate,
            "mutation_seed": mutation_seed,
            "disorientation_probability": disorientation_probability,
            "disorientation_seed": disorientation_seed,
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

def create_config_here(redo_config: bool=False, leaf_count: int=1000, sequence_length: int=50000, tree_height: float=0.1, query_count: int=200, core_count: int=8,
                       query_min_lenght: int=100, fragment_count: int=50, nick_freq: float=0.005, overhang_parameter: float=1.0, double_strand_deamination: float=0.0, single_strand_deamination: float=0.0,
                       iqtree_seed: int | None = None, pygargammel_seed: int | None = None, query_selection_seed: int | None=None,
                       mutation_rate: float | None = None, mutation_seed: int | None = None, disorientation_probability: float | None = None, disorientation_seed: int | None = None):

    # Get the path of the file that called this function
    base_dir = Path(inspect.stack()[1].filename).resolve().parent

    return create_config_at_path(base_dir, redo_config, leaf_count, sequence_length, tree_height, query_count, core_count,
                                 query_min_lenght, fragment_count, nick_freq, overhang_parameter, double_strand_deamination, single_strand_deamination,
                                 iqtree_seed, pygargammel_seed, query_selection_seed,
                                 mutation_rate, mutation_seed, disorientation_probability, disorientation_seed)

def modify_config_at_path(base_dir: Path, redo_config: bool=False, leaf_count: int | None = None, sequence_length: int | None = None, tree_height: float | None = None, query_count: int | None = None, core_count: int | None = None,
                          query_min_length: int | None = None, fragment_count: int | None = None, nick_freq: float | None = None, overhang_parameter: float | None = None, double_strand_deamination: float | None = None, single_strand_deamination: float | None = None,
                          iqtree_seed: int | None = None, pygargammel_seed: int | None = None, query_selection_seed: int | None=None,
                          mutation_rate: float | None = None, mutation_seed: int | None = None, disorientation_probability: float | None = None, disorientation_seed: int | None = None,
                          missing_references_selection_seed: int | None = None):
    config_path = base_dir / "config.yaml"

    if not redo_config:
        print(f"[INFO] Not modifying configuration at {config_path}")
        return config_path

    with config_path.open("r") as f:
        config = yaml.safe_load(f)

    if leaf_count is not None:
        config["leaf_count"] = leaf_count
    if sequence_length is not None:
        config["sequence_length"] = sequence_length
    if tree_height is not None:
        config["tree_height"] = tree_height
    if query_count is not None:
        config["query_count"] = query_count
    if core_count is not None:
        config["core_count"] = core_count
    if query_min_length is not None:
        config["query_min_length"] = query_min_length
    if fragment_count is not None:
        config["fragment_count"] = fragment_count
    if nick_freq is not None:
        config["nick_freq"] = nick_freq
    if overhang_parameter is not None:
        config["overhang_parameter"] = overhang_parameter
    if double_strand_deamination is not None:
        config["double_strand_deamination"] = double_strand_deamination
    if single_strand_deamination is not None:
        config["single_strand_deamination"] = single_strand_deamination
    if iqtree_seed is not None:
        config["iqtree_seed"] = iqtree_seed
    if pygargammel_seed is not None:
        config["pygargammel_seed"] = pygargammel_seed
    if query_selection_seed is not None:
        config["query_selection_seed"] = query_selection_seed
    if mutation_rate is not None:
        config["mutation_rate"] = mutation_rate
    if mutation_seed is not None:
        config["mutation_seed"] = mutation_seed
    if disorientation_probability is not None:
        config["disorientation_probability"] = disorientation_probability
    if disorientation_seed is not None:
        config["disorientation_seed"] = disorientation_seed
    if missing_references_selection_seed is not None:
        config["missing_references_selection_seed"] = missing_references_selection_seed

    with config_path.open("w") as f:
        yaml.dump(config, f, sort_keys=False)
    print(f"[INFO] Modified configuration at {config_path}")
    return config_path

