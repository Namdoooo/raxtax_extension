from raxtax_extension_prototype.simulator import run_simulation, create_config_here
from pathlib import Path

if __name__ == "__main__":
    config_path = Path(__file__).parent
    create_config_here(config_path, leaf_count=100, sequence_length=5000)
    run_simulation()