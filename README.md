# A formatter for Workflow Description Language (WDL)

![Status warning](https://img.shields.io/badge/Status-Unstable_(Under_development)-green)

This is an opinionated, lossless, formatter for [WDL](https://github.com/openwdl/wdl) that ensures consistency and small diffs between projects. 

> For now there is no automated way of styling or checking the style of WDL files according to these guidelines. It is up to the authors and reviewers to ensure the guidelines are adhered to. 
> From: [*BioWDL Style Guidelines*](https://biowdl.github.io/styleGuidelines.html)


`wdlfmt` aims to solve this problem.

## Installation

`wdlfmt` is currently under development and not recommended for production use. With that said, you can install and run the current version from Github:

```sh
git clone https://github.com/Chris1221/wdlfmt.git 
pip install -e wdlfmt
```

To format a simple WDL `v1.0` file, use the CLI interface. By default, the output is written to standard out, but the optional `-i` flag will format the file in place.

```sh
wdlfmt test/examples/test_md5.wdl 
```

Note that due to the project's early development status, you should probably not run `-i` and instead inspect the output carefully to ensure that your WDL files are not modified. 