# wdlfmt — a formatter for Workflow Description Language (WDL)

[![PyPI version](https://img.shields.io/pypi/v/wdlfmt.svg)](https://pypi.org/project/wdlfmt/) [![CI](https://github.com/Chris1221/wdlfmt/actions/workflows/python-package.yml/badge.svg)](https://github.com/Chris1221/wdlfmt/actions/workflows/python-package.yml) [![Python versions](https://img.shields.io/pypi/pyversions/wdlfmt.svg)](https://pypi.org/project/wdlfmt/) [![Downloads](https://static.pepy.tech/badge/wdlfmt)](https://pepy.tech/projects/wdlfmt) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`wdlfmt` is an opinionated, lossless formatter for [WDL v1.0](https://github.com/openwdl/wdl) that enforces consistency and targets the [BioWDL Style Guidelines](https://biowdl.github.io/styleGuidelines.html).

> For now there is no automated way of styling or checking the style of WDL files according to these guidelines.
> — *BioWDL Style Guidelines*

`wdlfmt` aims to solve this problem.

## Installation

```sh
pip install wdlfmt
```

For development, clone the repo and use [pixi](https://pixi.sh):

```sh
git clone https://github.com/Chris1221/wdlfmt.git
cd wdlfmt && pixi install
pixi run test
```

## Usage

By default, formatted output is written to stdout and a style compliance checklist is printed to stderr:

```sh
wdlfmt my_task.wdl
```

Format in place with `-i`:

```sh
wdlfmt -i my_task.wdl
```

Suppress the checklist with `--no-check`:

```sh
wdlfmt --no-check my_task.wdl
```

Redirect formatted WDL to a file while keeping the checklist visible:

```sh
wdlfmt my_task.wdl > formatted.wdl
```

## What the formatter does

`wdlfmt` rewrites WDL files with consistent style, preserving all comments:

| Rule | Example (before → after) |
|------|--------------------------|
| 4-space indentation | tabs / mixed spaces → 4 spaces |
| Heredoc command syntax | `command { ... }` → `command <<< ... >>>` |
| Double-quoted strings | `'hello'` → `"hello"` |
| Spaces around `=` | `key=value` → `key = value` |

## BioWDL style compliance checklist

After every format run, `wdlfmt` emits a per-rule checklist to stderr. Rules the formatter enforces are shown as confirmed guarantees; content rules that depend on the file's naming and structure are checked and reported:

```
BioWDL Style Guide Compliance
──────────────────────────────────────────────────────
  Formatter guarantees
    ✓  4-space indentation
    ✓  Heredoc (<<<) command syntax
    ✓  Double-quote string literals
    ✓  Spaces around = operator
  Content checks
    ✓  Task names are UpperCamelCase
    ✓  Workflow names are UpperCamelCase
    ✓  Struct names are UpperCamelCase
    ✗  Call aliases are lowerCamelCase
         Non-conforming aliases: myAlias
    ✓  Line length ≤ 100 chars
    !  set -e -o pipefail in multi-command blocks
         Missing in: block 1
    !  parameter_meta section present
         Missing in: task 'MyTask'
    ✓  docker defined in runtime blocks
──────────────────────────────────────────────────────
  1 failed  ·  2 warning(s)  ·  9 passed
```

**Symbols:** `✓` pass · `✗` fail (rule violated) · `!` warn (advisory)

### Content rules

| Rule | Level | Description |
|------|-------|-------------|
| Task names are UpperCamelCase | fail | `task myTask` → rename to `MyTask` |
| Workflow names are UpperCamelCase | fail | Same convention for workflows |
| Struct names are UpperCamelCase | fail | Same convention for structs |
| Call aliases are lowerCamelCase | fail/warn | `call Foo as Bar` fails; `call Foo` (no alias) warns |
| Line length ≤ 100 chars | fail | Reports offending line numbers |
| `set -e -o pipefail` in command blocks | warn | Advisory for multi-command blocks |
| `parameter_meta` section present | warn | Advisory per task/workflow |
| `docker` in runtime blocks | warn | Advisory per runtime block |

## Python API

```python
import wdlfmt

# Format a WDL string
formatted = wdlfmt.format_wdl_str(wdl_text)

# Run the style checker on already-formatted text
results = wdlfmt.check_style(formatted)
for r in results:
    print(r.rule, r.status.value, r.details)
```

## Technical overview

`wdlfmt` is built on [ANTLR4](https://www.antlr.org/) and a visitor-pattern formatter registry.

**Parsing.** The WDL v1.0 grammar (`wdlfmt/grammar/WdlV1Lexer.g4` and `WdlV1Parser.g4`) is compiled to Python by ANTLR4. Parsing produces a typed parse tree where every node is a strongly-typed context object (e.g. `TaskContext`, `Task_commandContext`).

**Comment preservation.** WDL comments (`#`) are placed on a separate ANTLR token channel (channel 2) and are invisible to the default parse tree walk. `wdlfmt` extracts them from the token stream before visiting the tree, injects them as lightweight `CommentContext` nodes at the correct positions, and then emits them as part of the formatted output. This makes formatting lossless.

**Formatter registry.** `wdlfmt/formatters/` contains a subclass of `Formatter` for each WDL context type (`TaskFormatter`, `WorkflowFormatter`, `StructFormatter`, etc.). Each subclass declares which context type it handles via a `formats` class attribute. The registry is built at import time by inspecting all `Formatter` subclasses, so adding support for a new context type requires only a new subclass — no wiring code.

**Command block formatting.** WDL `command <<<` blocks contain shell script. `wdlfmt` extracts the shell body, replaces WDL interpolation expressions (`~{...}`) with safe placeholders, passes the result through [`shfmt`](https://github.com/mvdan/sh) (bundled via `shfmt-py`), then restores the original expressions. This ensures shell code inside WDL tasks is also consistently formatted.

**Style checker.** The `StyleChecker` in `wdlfmt/checker.py` operates on the already-formatted text using regex — no re-parsing. This keeps it fast and decoupled from the formatter internals.
