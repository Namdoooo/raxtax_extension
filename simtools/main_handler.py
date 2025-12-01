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

def create_specific_main_at_path(base_dir: Path, func_name: str,redo_main: bool = False):
    script = f"""\
from simtools.simulator import {func_name}

if __name__ == "__main__":
    {func_name}()
        """

    main_path = base_dir / "main.py"

    if redo_main or not main_path.exists():
        main_path.write_text(script)
        print(f"[INFO] Created main.py at: {main_path}")

def create_executable_at_path(base_dir: Path, func_name: str, file_name: str, redo_executable: bool = False):
    script = f"""\
from simtools.simulator import {func_name}

if __name__ == "__main__":
    {func_name}()
        """

    executable_path = base_dir / file_name

    if redo_executable or not executable_path.exists():
        executable_path.write_text(script)
        print(f"[INFO] Created {file_name} at: {executable_path}")