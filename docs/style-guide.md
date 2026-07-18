# BioWDL Style Guide

`wdlfmt` targets the [BioWDL Style Guidelines](https://biowdl.github.io/styleGuidelines.html). After every format run it emits a compliance checklist to stderr showing which rules pass, fail, or need attention.

## Sample output

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
         Non-conforming aliases: MyAlias
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

---

## Formatter guarantees

These rules are enforced unconditionally by the formatter. They will always show `✓`.

### 4-space indentation

All block contents are indented with exactly 4 spaces per level. Tabs and mixed whitespace are rewritten.

```wdl title="Before"
task MyTask {
	input {
	  String name
	}
}
```

```wdl title="After"
task MyTask {
    input {
        String name
    }
}
```

### Heredoc command syntax

Command blocks are always written with `<<<` / `>>>` delimiters, never `{` / `}`.

```wdl title="Before"
command {
    echo hello
}
```

```wdl title="After"
command <<<
    echo hello
>>>
```

### Double-quoted string literals

Single-quoted strings are rewritten with double quotes.

```wdl title="Before"
String greeting = 'hello'
```

```wdl title="After"
String greeting = "hello"
```

### Spaces around `=`

Assignment operators in declarations and `call` input blocks always have a single space on each side.

```wdl title="Before"
String name=basename(file,".bed")
```

```wdl title="After"
String name = basename(file, ".bed")
```

---

## Content checks

These rules depend on the content of your WDL file. `wdlfmt` checks them and reports the result, but cannot auto-fix them.

### Task names are UpperCamelCase — `fail`

Every `task` declaration must start with an uppercase letter and use CamelCase.

```wdl title="Fail"
task calcMd5 { ... }   # ✗ should be CalcMd5
task my_task { ... }   # ✗ should be MyTask
```

```wdl title="Pass"
task CalcMd5 { ... }   # ✓
```

### Workflow names are UpperCamelCase — `fail`

Same convention as task names.

```wdl title="Fail"
workflow myWorkflow { ... }  # ✗
```

```wdl title="Pass"
workflow MyWorkflow { ... }  # ✓
```

### Struct names are UpperCamelCase — `fail`

```wdl title="Pass"
struct SampleInfo { ... }  # ✓
```

### Call aliases are lowerCamelCase — `fail` / `warn`

All `call` statements should have an `as` alias in lowerCamelCase. A missing alias is a warning; a non-conforming alias is a failure.

```wdl title="Fail"
call CalcMd5 as CalcMd5 { ... }  # ✗ alias must be lowerCamelCase
```

```wdl title="Warn"
call CalcMd5 { ... }  # ! missing 'as' alias
```

```wdl title="Pass"
call CalcMd5 as calcMd5 { ... }  # ✓
```

### Line length ≤ 100 chars — `fail`

Lines exceeding 100 characters are flagged with their line numbers.

### `set -e -o pipefail` in multi-command blocks — `warn`

Command blocks with more than one non-comment line should begin with `set -e -o pipefail` to ensure the task fails fast on any error.

```wdl title="Warn"
command <<<
    echo step1
    echo step2
>>>
```

```wdl title="Pass"
command <<<
    set -e -o pipefail
    echo step1
    echo step2
>>>
```

### `parameter_meta` section present — `warn`

Each `task` and `workflow` should document its inputs in a `parameter_meta` block.

```wdl title="Pass"
task MyTask {
    input {
        File inputFile
    }
    parameter_meta {
        inputFile: "The file to process."
    }
    command <<< ... >>>
}
```

### `docker` defined in runtime blocks — `warn`

Every `runtime` block should specify a `docker` image to ensure reproducibility.

```wdl title="Warn"
runtime {
    memory: "4G"
}
```

```wdl title="Pass"
runtime {
    docker: "ubuntu:22.04"
    memory: "4G"
}
```
