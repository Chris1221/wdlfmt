# Usage

## CLI

### Basic formatting

Format a WDL file and print the result to stdout:

```sh
wdlfmt my_task.wdl
```

By default, the formatted WDL goes to stdout and a [style compliance checklist](style-guide.md) goes to stderr, so they can be redirected independently:

```sh
# Save formatted WDL, keep checklist visible in the terminal
wdlfmt my_task.wdl > formatted.wdl

# Discard the checklist entirely
wdlfmt my_task.wdl 2>/dev/null
```

### Edit in place

```sh
wdlfmt -i my_task.wdl
```

### Multiple files

```sh
wdlfmt task1.wdl task2.wdl workflow.wdl
```

### Skip the checklist

```sh
wdlfmt --no-check my_task.wdl
```

### All flags

| Flag | Default | Description |
|------|---------|-------------|
| `files` (positional) | — | One or more WDL files to format |
| `-i`, `--in-place` | off | Edit files in place instead of printing to stdout |
| `--no-check` | off | Skip the BioWDL style guide compliance checklist |

## Python API

### Format a string

```python
import wdlfmt

wdl = """
version 1.0

task MyTask {
  input { String name }
  command <<< echo ~{name} >>>
}
"""

formatted = wdlfmt.format_wdl_str(wdl)
print(formatted)
```

### Format files on disk

```python
import wdlfmt

# Print to stdout (default behaviour)
wdlfmt.format_wdl(files=["my_task.wdl"])

# Edit in place
wdlfmt.format_wdl(files=["my_task.wdl"], in_place=True)

# Capture the formatted text
text = wdlfmt.format_wdl(files=["my_task.wdl"], return_object=True)
```

### Run the style checker

```python
import wdlfmt

formatted = wdlfmt.format_wdl_str(wdl_text)
results = wdlfmt.check_style(formatted)

for r in results:
    print(f"{r.status.value:5}  {r.rule}")
    if r.details:
        print(f"       {r.details}")
```

`check_style` returns a list of [`CheckResult`](api/checker.md) objects, each with `.rule`, `.status` (`PASS`, `FAIL`, or `WARN`), and `.details`.
