from raxtax_extension_prototype.simulator import run_simulation
from raxtax_extension_prototype.config_handler import create_config_here

if __name__ == "__main__":
    create_config_here(redo_config=False, leaf_count=1000, sequence_length=50000, tree_height=0.1, query_count=200, core_count=2,
                       query_min_lenght=100, fragment_count=50)
    run_simulation()