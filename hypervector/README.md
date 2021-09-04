Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Setup development environment

```sh
pip install -r requirements.lock.txt
```

## Running the pipeline

(stores reference values to Hypervector)

```sh
ploomber build --env--test false
```

(compares with reference values from Hypervector)

```sh
ploomber build
```

## Notes

* Once a task executes, it won't execute again unless the source code changes
* To force execution: `ploomber builf --force`
* To run a single task `ploomber task {name}` (e.g., `ploomber task fit`)
* To only run the on finish hook `ploomber task fit --on-finish`
