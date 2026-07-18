# Adding Formatters

Every WDL construct is formatted by a dedicated `Formatter` subclass. The registry is built automatically at import time, so adding a new formatter requires only a new class — no wiring code.

## The `Formatter` base class

```python
from abc import ABC, abstractmethod
from wdlfmt.formatters.common import Formatter

class Formatter(ABC):
    @abstractmethod
    def format(self, input, indent: int = 0) -> str:
        """Return the formatted string for this context."""
        pass

    @property
    @abstractmethod
    def formats(self):
        """The WdlV1Parser context class this formatter handles."""
        pass

    @property
    @abstractmethod
    def public(self):
        """True if this formatter is top-level (registered by default)."""
        pass
```

`formats` is the ANTLR-generated context class (e.g. `WdlV1Parser.StructContext`).

`public = True` means the formatter is registered in the top-level registry used by `WdlVisitor`. `public = False` is for sub-formatters that are only looked up from within another formatter's `format()` method via `collect_formatters(only_public=False)`.

## Example: `StructFormatter`

Here is the complete formatter for WDL `struct` declarations (`wdlfmt/formatters/struct.py`):

```python
from ..grammar.WdlV1Parser import WdlV1Parser
from wdlfmt.formatters.common import (
    Formatter, indent_text, CommentContext, collect_formatters,
)
from ..utils import get_raw_text


class StructFormatter(Formatter):
    formats = WdlV1Parser.StructContext
    public = True

    def format(self, input: WdlV1Parser.StructContext, indent: int = 0) -> str:
        formatted = f"struct {input.Identifier().getText()} {{\n"
        formatters = collect_formatters(False)  # include private formatters

        for child in input.children:
            if isinstance(child, CommentContext):
                formatted += formatters[str(type(child))].format(child, indent + 1, True)
                continue
            try:
                formatted += formatters[str(type(child))].format(child, indent + 1)
            except KeyError:
                pass  # skip terminal tokens (braces, whitespace)

        formatted += "}\n\n"
        return formatted


class StructDeclsContext(Formatter):
    formats = WdlV1Parser.Unbound_declsContext
    public = False  # only used from within StructFormatter

    def format(self, input: WdlV1Parser.Unbound_declsContext, indent: int = 0):
        return indent_text(" ".join(get_raw_text(input).split()) + "\n", indent)
```

## Step-by-step: adding a new formatter

**1. Identify the context class.**

Find the grammar rule in `wdlfmt/grammar/WdlV1Parser.g4` or look at the ANTLR-generated `WdlV1Parser.py`. Every grammar rule `foo` produces a `FooContext` class, accessible as `WdlV1Parser.FooContext`.

**2. Create the formatter class.**

Add it to the appropriate file in `wdlfmt/formatters/` (or create a new module):

```python
from ..grammar.WdlV1Parser import WdlV1Parser
from wdlfmt.formatters.common import Formatter, indent_text

class MyNewFormatter(Formatter):
    formats = WdlV1Parser.MyNewContext
    public = True  # or False if called from another formatter

    def format(self, input: WdlV1Parser.MyNewContext, indent: int = 0) -> str:
        # Build and return the formatted string.
        return f"my_keyword {input.Identifier().getText()}\n"
```

**3. Import the module in `wdlfmt/formatters/__init__.py` (if adding a new file).**

The registry is populated via subclass inspection — the class just needs to be imported somewhere before `collect_formatters()` runs. The `wdlfmt/visitor.py` top-level imports (`from wdlfmt.formatters import struct, task, workflow`) exist precisely for this side effect.

If you add a new module, import it there:

```python
# wdlfmt/visitor.py
from wdlfmt.formatters import struct, task, workflow, my_new_module  # noqa: F401
```

**4. Write a test.**

Add a snapshot pair in `test/snapshots/` (`my_feature.input.wdl` + `my_feature.expected.wdl`) and run:

```sh
pixi run test
```

## Useful helpers

| Function | Location | Purpose |
|----------|----------|---------|
| `indent_text(text, level, spaces=4)` | `common.py` | Indent every line of `text` by `level * spaces` spaces |
| `collect_formatters(only_public)` | `common.py` | Return the full formatter dict (set `only_public=False` inside a formatter) |
| `subset_children(children, types)` | `common.py` | Filter a children list by one or more context types |
| `get_raw_text(ctx)` | `utils.py` | Return the raw source text for a context node |
