"""
Assuming there already exists some [pixi] project (preferably from a git repo already initialized), here's what'll happen:
    1. add my ruff config
    2. add pipelight (HCL) preloaded with ruff formatting + linting and initialize it from within the project

Therefore the flow would be:
    1. Initialize a Git repo
    2. Initialize Pixi project in there
    3. `px init`
    4. Change ruff `target-version` in ruff.toml
"""
import subprocess
import os
import shutil
from px.constants import PX_PROJECT_ROOT


def copy_and_modify_file(source_path: str, dest_path: str, new_first_line: str):
    # Copy the file
    shutil.copy2(source_path, dest_path)
    
    # Open the copied file in read mode
    with open(dest_path, 'r') as file:
        lines = file.readlines()
    
    # Modify the first line
    lines[0] = new_first_line + '\n'
    
    # Open the file again in write mode
    with open(dest_path, 'w') as file:
        file.writelines(lines)


if __name__ == "__main__":
    pyver: str = input("Python Target Version (for ruff)? ").replace(" ", "").replace(".", "")
    fmted_pyver: str = f"py{pyver}"
    
    # Add ruff config
    copy_and_modify_file(
        source_path=f"{PX_PROJECT_ROOT}/ruff.toml",
        dest_path="./ruff.toml",
        new_first_line=f'target-version = "{fmted_pyver}"'
    )

    # Setup pipelight
    
    # Copy the pipelight file in this repo
    subprocess.run(f"cp {PX_PROJECT_ROOT}/pipelight.hcl ./pipelight.hcl", shell=True)
    
    # Enable git hooks
    subprocess.run("pipelight enable git-hooks && pipelight ls")

    
