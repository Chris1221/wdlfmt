from ..grammar.WdlV1Parser import WdlV1Parser
from .shell_formatter import ShfmtFormatter
from wdlformat.formatters.common import (
    Formatter,
    indent_text,
    subset_children,
    CommentContext,
    collect_formatters,
)
from typing import Dict, Type
import wdlformat

from ..utils import get_raw_text


class VersionFormatter(Formatter):
    formats = WdlV1Parser.VersionContext
    public = True

    def format(self, input: WdlV1Parser.VersionContext, indent: int = 0) -> str:
        return f"{input.VERSION().getText()} {input.ReleaseVersion().getText()}\n\n\n"


class TaskFormatter(Formatter):
    formats = WdlV1Parser.TaskContext
    public = True

    def format(self, input: WdlV1Parser.TaskContext, indent: int = 0) -> str:
        """Format a task.

        This is an opinionated formatter that will format the task as follows:
        - Input
        - Command
        - Output
        - Runtime
        - Parameter meta

        The order of the sections is not configurable.
        """
        formatted = f"task {input.Identifier().getText()} {{\n"
        formatters = collect_formatters(False)

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
                    raise NotImplementedError("Multiple children not implemented")

            else:
                # If the child has no children then it is a single line
                # and can be formatted directly
                if str(type(child)) in formatters:
                    formatted += formatters[str(type(child))].format(child, indent + 1)

        formatted += "}\n\n"
        return formatted


class OutputFormatter(Formatter):
    formats = [WdlV1Parser.Task_outputContext, WdlV1Parser.Workflow_outputContext]
    public = True

    def format(self, input: WdlV1Parser.Task_outputContext, indent: int = 1) -> str:
        formatters = collect_formatters(False)

        formatted = ""

        for child in input.children:
            if isinstance(child, CommentContext):
                formatted += formatters[str(type(child))].format(child, indent, True)

            if isinstance(child, WdlV1Parser.Bound_declsContext):
                formatted += formatters[str(type(child))].format(child, indent)

        return indent_text(
            f"output {{\n{indent_text(''.join(formatted))}}}\n\n", indent
        )


class InputFormatter(Formatter):
    formats = [WdlV1Parser.Task_inputContext, WdlV1Parser.Workflow_inputContext]
    public = True

    def format(self, input: WdlV1Parser.Task_inputContext, indent: int = 1) -> str:
        formatters = collect_formatters(False)

        declsContexts = subset_children(input.children, WdlV1Parser.Any_declsContext)

        formatted = ""

        for child in input.children:
            if isinstance(child, CommentContext):
                formatted += formatters[str(type(child))].format(child, indent, True)

            if isinstance(child, WdlV1Parser.Any_declsContext):
                formatted += formatters[str(type(child))].format(child, indent)

        # decls = "".join(
        #     [
        #         formatters[declsContext.__class__].format(declsContext)
        #         for declsContext in declsContexts
        #     ]
        # )

        # breakpoint()

        return indent_text(f"input {{\n{indent_text(''.join(formatted))}}}\n\n", indent)


class CommandFormatter(Formatter):
    formats = WdlV1Parser.Task_commandContext
    public = True

    def format(self, input: WdlV1Parser.Task_commandContext, indent: int = 2) -> str:

        commands = subset_children(
            input.children,
            [
                WdlV1Parser.Task_command_string_partContext,
                WdlV1Parser.Task_command_expr_with_stringContext,
            ],
        )

        shell_script = "".join([get_raw_text(i) for i in commands])

        formatted_command = ShfmtFormatter(shell_script).format()
        formatted = "command <<<\n"
        formatted += indent_text(formatted_command, 1)
        formatted += ">>>\n\n"

        return indent_text(formatted, 1)


class RuntimeFormatter(Formatter):
    formats = WdlV1Parser.Task_runtimeContext
    public = True

    def format(self, input: WdlV1Parser.Task_runtimeContext, indent: int = 1) -> str:
        formatters = collect_formatters(False)

        formatted = ""

        for child in input.children:
            if isinstance(child, CommentContext):
                formatted += formatters[str(type(child))].format(child, indent, True)

            if isinstance(child, WdlV1Parser.Task_runtime_kvContext):
                formatted += formatters[str(type(child))].format(child, indent)

        return indent_text(
            f"runtime {{\n{indent_text(''.join(formatted))}}}\n\n", indent
        )


class RuntimeKVContext(Formatter):
    formats = WdlV1Parser.Task_runtime_kvContext
    public = False

    def format(self, input: WdlV1Parser.Task_runtime_kvContext, indent: int = 1) -> str:
        formatters = collect_formatters(False)

        key = input.Identifier().getText()
        value = subset_children(input.children, WdlV1Parser.ExprContext)[0]

        return indent_text(
            f"{key}: {formatters[str(value.__class__)].format(value)}\n", indent
        )


class ExprContextFormatter(Formatter):
    formats = WdlV1Parser.ExprContext
    public = False

    def format(self, input: WdlV1Parser.ExprContext, indent: int = 0) -> str:
        expression = " ".join([child.getText() for child in input.children])

        # Remove the extra space at the end of the expression
        expression = expression.strip()

        # Ensure that quotations are double not single quotes
        # I don't know if there will be any internal cases
        # but just in case.
        expression = list(expression)
        expression[0] = expression[0].replace("'", '"')
        expression[-1] = expression[-1].replace("'", '"')
        expression = "".join(expression)

        return expression


class BoundContextFormatter(Formatter):
    formats = WdlV1Parser.Bound_declsContext
    public = True

    def format(self, input: WdlV1Parser.Bound_declsContext, indent: int = 1) -> str:
        formatted = indent_text(
            " ".join([child.getText() for child in input.children]), level=indent
        )
        return f"{formatted}\n"


class AnyContextFormatter(Formatter):
    formats = WdlV1Parser.Any_declsContext
    public = False

    def format(self, input: WdlV1Parser.Any_declsContext, indent: int = 2) -> str:
        formatted = indent_text(
            " ".join([child.getText() for child in input.children[0].children]),
            level=indent,
        )
        return f"{formatted}\n"


class CommentFormatter(Formatter):
    formats = wdlformat.formatters.common.CommentContext
    public = True

    def format(
        self, input: CommentContext, indent: int = 0, force: bool = False
    ) -> str:
        if input.top_level or force:
            return indent_text("#" + input.getText().strip().strip("#") + "\n", indent)
        else:
            return ""
