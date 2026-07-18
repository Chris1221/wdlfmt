# Installation

## From PyPI

```sh
pip install wdlfmt
```

!!! note
    pip >= 23.0 is required. If the package installs as `UNKNOWN`, upgrade pip first:
    ```sh
    pip install --upgrade pip
    ```

Verify the install:

```sh
wdlfmt --help
```

## Development setup

Clone the repo and use [pixi](https://pixi.sh) to create a fully reproducible environment:

```sh
git clone https://github.com/Chris1221/wdlfmt.git
cd wdlfmt
pixi install
```

Run the test suite:

```sh
pixi run test
```

Run the linter:

```sh
pixi run lint
```

Format a file using the local development version:

```sh
pixi run wdlfmt my_task.wdl
```

## Dependencies

`wdlfmt` installs three runtime dependencies automatically:

| Package | Purpose |
|---------|---------|
| `antlr4-python3-runtime==4.12` | ANTLR4 runtime for WDL parsing |
| `shfmt-py` | Bundles the [`shfmt`](https://github.com/mvdan/sh) shell formatter binary used for command blocks |
