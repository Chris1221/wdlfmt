from ..grammar.WdlV1Parser import WdlV1Parser
from wdlformat.formatters.common import (
    Formatter,
    indent_text,
    subset_children,
    collect_formatters,
)
from typing import Dict
from ..utils import get_raw_text


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
                    pass
            else:
                # If the child has no children then it is a section
                if str(type(child)) in formatters:
                    formatted += formatters[str(type(child))].format(child, indent + 1)

        formatted += "}\n\n"
        return formatted


class ParameterMetaFormatter(Formatter):
    formats = WdlV1Parser.Parameter_metaContext
    public = False

    def format(self, input: WdlV1Parser.Parameter_metaContext, indent: int = 0) -> str:
        formatters = collect_formatters(False)

        formatted = f"parameter_meta {{\n"
        for child in input.children:
            if "Comment" in str(type(child)):
                formatted += f"{child.getText()}\n"
            elif "Meta_kvContext" in str(type(child)):
                formatted += formatters[str(type(child))].format(child, indent)

        formatted += "}\n\n"
        formatted = indent_text(formatted, indent)
        return formatted


class MetaKVFormatter(Formatter):
    formats = WdlV1Parser.Meta_kvContext
    public = False

    def format(self, input: WdlV1Parser.Meta_kvContext, indent: int = 0) -> str:
        name = input.children[0].getText()
        value = input.children[2].getText()
        formatted = indent_text(f"{name}: {value}\n", indent)
        return formatted


class Inner_workflowFormatter(Formatter):
    formats = WdlV1Parser.Inner_workflow_elementContext
    public = False

    def format(
        self, input: WdlV1Parser.Inner_workflow_elementContext, indent: int = 0
    ) -> str:
        formatted = ""
        formatters = collect_formatters(False)

        for child in input.children:
            if "Comment" in str(type(child)):
                formatted += f"{child.getText()}\n"

            else:
                formatted += formatters[str(type(child))].format(child, indent)

        return formatted


class CallFormatter(Formatter):
    formats = WdlV1Parser.CallContext
    public = False

    def format(self, input: WdlV1Parser.CallContext, indent: int = 0) -> str:

        name_context = subset_children(input.children, WdlV1Parser.Call_nameContext)[
            0
        ].getText()
        alias_context = subset_children(input.children, WdlV1Parser.Call_aliasContext)
        body_context = subset_children(input.children, WdlV1Parser.Call_bodyContext)[0]

        # If there's an alias, we have to format it as such
        if len(alias_context) > 0:
            alias_name = get_raw_text(alias_context[0]).strip().split()[1]
            formatted = f"call {name_context} as {alias_name} {{\n"

        else:
            formatted = f"call {name_context} {{\n"

        formatters = collect_formatters(False)

        # Now go through the statements in the body and format them
        for child in body_context.children:
            if "Comment" in str(type(child)):
                formatted += f"{child.getText()}\n"

            elif str(type(child)) == "<class 'antlr4.tree.Tree.TerminalNodeImpl'>":
                pass

            else:
                formatted += formatters[str(type(child))].format(child, indent)

        # Remove the last comma
        formatted = formatted.rstrip(",\n")
        formatted += "\n}\n\n"
        formatted = indent_text(formatted, indent)
        return formatted


class CallInputFormatter(Formatter):
    formats = WdlV1Parser.Call_inputsContext
    public = False

    def format(self, input: WdlV1Parser.Call_inputsContext, indent: int = 0) -> str:
        formatted = "input:\n"

        inputs = subset_children(input.children, WdlV1Parser.Call_inputContext)

        for input in inputs:
            name = input.getText().split("=")[0].strip()
            expr = subset_children(input.children, WdlV1Parser.ExprContext)[0].getText()
            formatted += indent_text(f"{name} = {str(expr)},\n", indent)

        return indent_text(formatted, indent)

        # There may not be an alias
