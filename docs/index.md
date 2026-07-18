# wdlfmt

[![PyPI version](https://img.shields.io/pypi/v/wdlfmt.svg)](https://pypi.org/project/wdlfmt/)
[![CI](https://github.com/Chris1221/wdlfmt/actions/workflows/python-package.yml/badge.svg)](https://github.com/Chris1221/wdlfmt/actions/workflows/python-package.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An opinionated, lossless formatter for [WDL v1.0](https://github.com/openwdl/wdl) that enforces consistency and checks compliance with the [BioWDL Style Guidelines](https://biowdl.github.io/styleGuidelines.html).

> For now there is no automated way of styling or checking the style of WDL files according to these guidelines.
> — *BioWDL Style Guidelines*

`wdlfmt` aims to solve this problem.

## Quick start

```sh
pip install wdlfmt
wdlfmt my_task.wdl
```

Formatted WDL is written to stdout. A style compliance checklist appears on stderr.

## Navigation

**General users**

- [Installation](installation.md) — pip install, dev setup, verification
- [Usage](usage.md) — CLI flags, Python API, common patterns
- [Style Guide](style-guide.md) — the 12 BioWDL rules wdlfmt enforces and checks

**Extending wdlfmt**

- [Architecture](technical/architecture.md) — how the pipeline works end to end
- [Visitor Pattern](technical/visitor.md) — how the parse tree is walked and formatted
- [Adding Formatters](technical/formatters.md) — how to add support for a new WDL context
- [Grammar & ANTLR4](technical/grammar.md) — the grammar files and how to regenerate them
