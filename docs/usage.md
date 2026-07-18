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

### Check mode (CI enforcement)

Verify that files are already correctly formatted without modifying them:

```sh
wdlfmt --check my_task.wdl
# or
wdlfmt -c my_task.wdl
```

Exits 0 if all files are correctly formatted, 1 if any would be changed. This is the intended way to enforce formatting in CI.

**GitHub Actions:**

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'

- name: Install wdlfmt
  run: pip install wdlfmt

- name: Check WDL formatting
  run: wdlfmt --check **/*.wdl
```

**CircleCI:**

```yaml
jobs:
  check-wdl-formatting:
    docker:
      - image: cimg/python:3.12
    steps:
      - checkout
      - run:
          name: Install wdlfmt
          command: pip install wdlfmt
      - run:
          name: Check WDL formatting
          command: wdlfmt --check **/*.wdl
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
| `-c`, `--check` | off | Exit 1 if any file would be reformatted; do not write output |
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
