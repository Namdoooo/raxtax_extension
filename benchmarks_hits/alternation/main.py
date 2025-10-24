from pathlib import Path

from simtools.simulator import run_main_list

if __name__ == "__main__":
    main_list = []
    base_dir = Path(__file__).resolve().relative_to(Path.cwd()).parent
    for i in range(11, 31):
        main_path = base_dir / f"iteration{i}"
        main_list.append(main_path)
        print(main_path)

    run_main_list(main_list)
