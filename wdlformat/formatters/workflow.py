from ..grammar.WdlV1Parser import WdlV1Parser
from .shell_formatter import ShfmtFormatter
from wdlformat.formatters.common import (
    Formatter,
    indent_text,
    subset_children,
    CommentContext,
)
from typing import Dict, Type
import wdlformat


class WorkflowFormatter(Formatter):
    formats = WdlV1Parser.WorkflowContext
    public = True

    def format(self, input: WdlV1Parser.WorkflowContext, indent: int = 0) -> str:
        """Format a workflow.
        This is an opinionated formatter that will format the workflow as follows:
        - Input
        - Output
        - Call
        - Scatter
        - If
        - WorkflowElement
        The order of the sections is not configurable.
        """
        formatted = f"\nworkflow {input.Identifier().getText()} {{\n"
        formatters = collect_workflow_formatters()

        for child in input.children:

            # If the child itself has children then
            # it is a block section and must be formatted separately

            if "Comment" in str(type(child)):
                formatted += formatters[str(type(child))].format(
                    child, indent + 1, True
                )
                continue

            if hasattr(child, "children"):
                if len(child.children) == 1:
                    # If the child has only one child then it is a section
                    grandchild = child.children[0]
                    if str(type(grandchild)) in formatters:
                        formatted += formatters[str(type(grandchild))].format(
                            grandchild, indent + 1
                        )
                else:
                    # I don't know what case would have multiple
                    # children yet but I'm sure it will come up
                    pass
            else:
                # If the child has no children then it is a section
                if str(type(child)) in formatters:
                    formatted += formatters[str(type(child))].format(child, indent + 1)

        formatted += "}\n\n"
        return formatted


def collect_workflow_formatters(only_public: bool = True):
    """Collect all the formatters for tasks"""
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
