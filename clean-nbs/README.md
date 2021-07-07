# On writing clean Jupyter notebooks (sample code)

## Layout

`exploratory/` - Exploratory notebooks (raw data reference)
`src/` - Utility code
`tasks/` - Pipeline tasks (`.py` scripts that can open as notebooks in Jupyter)
`tests/` - Tests for code in `src/`

## Instructions

Install:

```sh
pip install -r requirements.lock.txt
pip install -e .
```

Run pipeline:

```sh
ploomber build
```