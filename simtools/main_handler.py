from pathlib import Path

def create_main_at_path(base_dir: Path, redo_main: bool = False):
    script = """\
from simtools.simulator import run_simulation

if __name__ == "__main__":
    run_simulation()
    """

    main_path = base_dir / "main.py"

    if redo_main or not main_path.exists():
        main_path.write_text(script)
        print(f"[INFO] Created main.py at: {main_path}")
