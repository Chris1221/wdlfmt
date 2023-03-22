# A module for struct formatters
from ..grammar.WdlV1Parser import WdlV1Parser
from .shell_formatter import ShfmtFormatter
from wdlformat.formatters.common import (
    Formatter,
    indent_text,
    subset_children,
    CommentContext,
)
from typing import Dict, Type
from ..utils import get_raw_text


class StructFormatter(Formatter):
    formats = WdlV1Parser.StructContext
    public = True

    def format(self, input: WdlV1Parser.StructContext, indent: int = 0) -> str:
        """Format a struct."""

        formatted = f"struct {input.Identifier().getText()} {{\n"
        formatters = collect_struct_formatters(False)

        for child in input.children:
            if isinstance(child, CommentContext):
                formatted += formatters[str(type(child))].format(
                    child, indent + 1, True
                )
                continue

            try:
                formatted += formatters[str(type(child))].format(child, indent + 1)
            except KeyError:
                pass

        formatted += "}\n\n"
        return formatted


class StructDeclsContext(Formatter):
    formats = WdlV1Parser.Unbound_declsContext
    public = False

    def format(self, input: WdlV1Parser.Unbound_declsContext, indent: int = 0):
        return indent_text(" ".join(get_raw_text(input).split()) + "\n", indent)


def collect_struct_formatters(only_public: bool = True):
    """Collect all the formatters for structs"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        if only_public and not formatter.public:
            continue

        if isinstance(formatter().formats, list):
            for format in formatter().formats:
                formatters[str(format)] = formatter()
        else:
            formatters[str(formatter().formats)] = formatter()

    return formatters
