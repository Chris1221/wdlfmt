from .grammar.WdlV1Parser import WdlV1Parser, ParserRuleContext
from abc import ABC, abstractmethod


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


class VersionFormatter(Formatter):
    formats = WdlV1Parser.VersionContext

    def format(self, input: WdlV1Parser.VersionContext, indent: int = 0) -> str:
        return f"{input.VERSION().getText()} {input.ReleaseVersion().getText()}\n"


class OutputFormatter(Formatter):
    formats = WdlV1Parser.Task_outputContext

    def format(self, input: WdlV1Parser.Task_outputContext, indent: int = 1) -> str:
        formatters = create_formatters_dict()

        declsContexts = subset_children(input.children, WdlV1Parser.Bound_declsContext)
        decls = "".join(
            [
                formatters[declsContext.__class__].format(declsContext)
                for declsContext in declsContexts
            ]
        )

        return indent_text(f"output {{\n{indent_text(''.join(decls))}}}\n", indent)


class InputFormatter(Formatter):
    formats = WdlV1Parser.Task_inputContext

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


class BoundContextFormatter(Formatter):
    formats = WdlV1Parser.Bound_declsContext

    def format(self, input: WdlV1Parser.Bound_declsContext, indent: int = 2) -> str:
        formatted = indent_text(
            " ".join([child.getText() for child in input.children]), level=indent
        )
        return f"{formatted}\n"


class AnyContextFormatter(Formatter):
    formats = WdlV1Parser.Any_declsContext

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


def create_formatters_dict():
    """Create a dictionary of all available formatters"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        formatters[formatter().formats] = formatter()
    return formatters
