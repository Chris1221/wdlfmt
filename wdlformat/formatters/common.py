from ..grammar.WdlV1Parser import WdlV1Parser, ParserRuleContext
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

    @property
    @abstractmethod
    def public(self):
        """Whether or not the formatter should be used by default"""
        pass


def collect_common_formatters():
    """Collect all the formatters for tasks"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        if formatter().public:
            formatters[formatter().formats] = formatter()
    return formatters


def subset_children(children, types):
    return [i for i in children if isinstance(i, types)]


def indent_text(text, level=0, spaces=4):
    return "".join([f"{' '*spaces*level}{line}" for line in text.splitlines(True)])


def create_formatters_dict():
    """Create a dictionary of all formatters"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        formatters[formatter().formats] = formatter()
    return formatters


class MetaCommentFormatter(Formatter):
    formats = WdlV1Parser.Meta_stringContext
    public = True

    def format(self, input: WdlV1Parser.Meta_stringContext, indent: int = 0) -> str:
        return f"# {input.getText()}\n"
