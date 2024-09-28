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

import os
import shutil
import subprocess


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


RUFF_TOML: str = '''
line-length = 99
indent-width = 4

# Respect the gitignore by not messing with that stuff
# This is already true by default
respect-gitignore = true

[format]
# Like Black, indent with spaces, rather than tabs.
indent-style = "space"

# Like Black, respect magic trailing commas.
skip-magic-trailing-comma = false

# Like Black, automatically detect the appropriate line ending.
line-ending = "auto"

# Screw yall we preserve quotes here
quote-style = "preserve"

[lint]
# Linting rules we are using
select = [
  "E4",
  "E7",
  "E9",
  "F",  # flake8
  "I",  # isort
  "B",  # flake8-bugbear
  "C4", # flake8-comprehensions
  #"NPY",   # numpy
  #"PD",    # pandas
  "FAST",  # fastapi
  "W191", # tab indentation
  "W291", # trailing whitespace (--fix this)
  "W605", # invalid escape sequence
]

# Linting rules we are ignoring
ignore = [
  "F401",  # unused imports; can just deal w/ that manually
  "E712",  # if a is True. sometimes syntax looks better this way
  "E722",  # allow the bare except if you aint using it
  "E731",  # lambda assignment. screw yall i can do whatever i want
  "C417",  # unnecessary-map; it seems ok syntactically and more readable
]

# Only these rules are fixable when doing `ruff check --fix`
fixable = [
  "E401",  # multiple imports on 1 line
  "E703",  # unnecessary semicolon
  "E711",  # None comparison should be `cond is None`
  "I",     # anything under import sorting
  "W191",  # indentation contains tabs rather than spaces
  "W291",  # trailing whitespace
]
'''

PIPELIGHT_HCL: str = """pipelines = [
  {
    name = "fmt-n-lint"
    steps = [
      {
        name     = "format"
        commands = ["ruff format px"]
      },
      {
        name     = "lint"
        commands = ["ruff check px --fix"]
      }
    ]
    triggers = [{
      branches = ["main", "dev"]
      actions  = ["pre-commit", "pre-push"]
    }]
  }
]
"""

if __name__ == "__main__":
    pyver: str = input("Python Target Version (for ruff)? ").replace(" ", "")

    # Add to the end if it doesn't do it right
    if pyver.count(".") <= 1:
        pyver += "."

    pyver = pyver[: pyver.rindex(".")].replace(".", "")

    fmted_pyver: str = f"py{pyver}"

    RUFF_TOML = f'target-version = "{fmted_pyver}"\n' + RUFF_TOML

    # Add ruff config
    with open("./ruff.toml", "w") as file:
        file.write(RUFF_TOML)

    # Setup pipelight

    # Copy the pipelight file in this repo
    with open("./pipelight.hcl", "w") as file:
        file.write(PIPELIGHT_HCL)

    # Enable git hooks
    subprocess.run("pipelight enable git-hooks && pipelight ls", shell=True)
