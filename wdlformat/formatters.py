from .grammar.WdlV1Parser import WdlV1Parser
from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, input) -> str:
        """Logic for formatting the input"""
        pass

    @property
    @abstractmethod
    def formats(self):
        """Class of the input to format"""
        pass

    @property
    @abstractmethod
    def indent(self):
        """Indentation to use for formatting"""
        pass


class VersionFormatter(Formatter):
    formats = WdlV1Parser.VersionContext
    indent = 0

    def format(self, input) -> str:
        return f"{input.VERSION().getText()} {input.ReleaseVersion().getText()}\n"


class OutputFormatter(Formatter):
    formats = WdlV1Parser.Task_outputContext
    indent = 1

    def format(self, input) -> str:
        formatters = create_formatters_dict()

        declsContexts = subset_children(input.children, WdlV1Parser.Bound_declsContext)
        decls = "".join(
            [
                formatters[declsContext.__class__].format(declsContext)
                for declsContext in declsContexts
            ]
        )

        return indent(f"output {{\n{indent(''.join(decls))}}}\n", self.indent)


class BoundContextFormatter(Formatter):
    formats = WdlV1Parser.Bound_declsContext
    indent = 2

    def format(self, input) -> str:
        formatted = indent(
            " ".join([child.getText() for child in input.children]), level=self.indent
        )
        return f"{formatted}\n"


def subset_children(children, types):
    return [i for i in children if isinstance(i, types)]


def indent(text, level=0, spaces=4):
    return "".join([f"{' '*spaces*level}{line}" for line in text.splitlines(True)])


def create_formatters_dict():
    """Create a dictionary of all available formatters"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        formatters[formatter().formats] = formatter()
    return formatters
