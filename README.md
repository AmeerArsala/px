# px

npx for python


## Installation

Prerequisites: [pipelight](https://pipelight.dev)

```bash
pip install python-px
```

## Add a Template

1. Fork this repository
2. Add a python script to `px/templates/your_template.py`.
3. Make a pull request to merge into main
4. Once accepted, you'll be able to do `px init your_template`

## Development

Must have [pixi](https://pixi.sh) and [pipelight](https://pipelight.dev) installed.
Then do:

```bash
pixi install
pixi shell --change-ps1=false -e dev
```
