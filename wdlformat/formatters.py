from .grammar.WdlV1Parser import WdlV1Parser, ParserRuleContext
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile, mkdtemp
from .shell_formatter import ShfmtFormatter
from os import remove


class Formatter(ABC):
    @abstractmethod
    def format(self, input: ParserRuleContext, indent: int = 0) -> str:
        """Logic for formatting the input"""
        pass

    @property
    @abstractmethod
    def formats(self):
        """Class of the input to format"""
        pass

    @property
    @abstractmethod
    def public(self):
        """Whether or not the formatter should be used by default"""
        pass


class VersionFormatter(Formatter):
    formats = WdlV1Parser.VersionContext
    public = True

    def format(self, input: WdlV1Parser.VersionContext, indent: int = 0) -> str:
        return f"{input.VERSION().getText()} {input.ReleaseVersion().getText()}\n\n"


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

        The order of the sections is not configurable.
        """
        # task name {
        #   input {
        #   }
        #   command {
        #   }
        #   output {
        #   }
        #   runtime {
        #    }
        # }
        formatted = f"task {input.Identifier().getText()} {{\n"
        formatters = create_public_formatters_dict()

        for child in input.children:
            if type(child) in formatters:
                formatted += formatters[type(child)].format(child, indent=1)

        formatted += "}\n\n"
        return formatted


class OutputFormatter(Formatter):
    formats = WdlV1Parser.Task_outputContext
    public = True

    def format(self, input: WdlV1Parser.Task_outputContext, indent: int = 1) -> str:
        formatters = create_formatters_dict()

        declsContexts = subset_children(input.children, WdlV1Parser.Bound_declsContext)
        decls = "".join(
            [
                formatters[declsContext.__class__].format(declsContext)
                for declsContext in declsContexts
            ]
        )

        return indent_text(f"output {{\n{indent_text(''.join(decls))}}}\n\n", indent)


class InputFormatter(Formatter):
    formats = WdlV1Parser.Task_inputContext
    public = True

    def format(self, input: WdlV1Parser.Task_inputContext, indent: int = 1) -> str:
        formatters = create_formatters_dict()

        declsContexts = subset_children(input.children, WdlV1Parser.Any_declsContext)
        decls = "".join(
            [
                formatters[declsContext.__class__].format(declsContext)
                for declsContext in declsContexts
            ]
        )

        return indent_text(f"input {{\n{indent_text(''.join(decls))}}}\n\n", indent)


class CommandFormatter(Formatter):
    formats = WdlV1Parser.Task_commandContext
    public = True

    def format(self, input: WdlV1Parser.Task_commandContext, indent: int = 2) -> str:

        command_part_1 = subset_children(
            input.children, WdlV1Parser.Task_command_string_partContext
        )
        command_part_2 = subset_children(
            input.children, WdlV1Parser.Task_command_expr_with_stringContext
        )

        shell_script = "".join(
            [
                f"{command_part_1[i].getText()}{command_part_2[i].getText()}"
                for i in range(len(command_part_1))
            ]
        )

        formatted_command = ShfmtFormatter(shell_script).format()

        formatted = "command <<<\n"
        formatted += indent_text(formatted_command, 1)
        formatted += ">>>\n\n"

        return indent_text(formatted, 1)


class RuntimeFormatter(Formatter):
    formats = WdlV1Parser.Task_runtimeContext
    public = True

    def format(self, input: WdlV1Parser.Task_runtimeContext, indent: int = 1) -> str:
        formatters = create_formatters_dict()

        runtime_kvContexts = subset_children(
            input.children, WdlV1Parser.Task_runtime_kvContext
        )
        runtime_kv = "".join(
            [
                formatters[runtime_kvContext.__class__].format(runtime_kvContext)
                for runtime_kvContext in runtime_kvContexts
            ]
        )

        return indent_text(
            f"runtime {{\n{indent_text(''.join(runtime_kv))}}}\n\n", indent
        )


class RuntimeKVContext(Formatter):
    formats = WdlV1Parser.Task_runtime_kvContext
    public = False

    def format(self, input: WdlV1Parser.Task_runtime_kvContext, indent: int = 1) -> str:
        formatters = create_formatters_dict()

        key = input.Identifier().getText()
        value = subset_children(input.children, WdlV1Parser.ExprContext)[0]

        return indent_text(
            f"{key}: {formatters[value.__class__].format(value)}\n", indent
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
    public = False

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


def subset_children(children, types):
    return [i for i in children if isinstance(i, types)]


def indent_text(text, level=0, spaces=4):
    return "".join([f"{' '*spaces*level}{line}" for line in text.splitlines(True)])


def create_public_formatters_dict():
    """Create a dictionary of all public formatters"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        if formatter.public:
            formatters[formatter().formats] = formatter()
    return formatters


def create_formatters_dict():
    """Create a dictionary of all formatters"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        formatters[formatter().formats] = formatter()
    return formatters
