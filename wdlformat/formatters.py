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


class VersionFormatter(Formatter):
    formats = WdlV1Parser.VersionContext

    def format(self, input) -> str:
        return f"{input.VERSION().getText()} {input.ReleaseVersion().getText()}\n"


def create_formatters_dict():
    """Create a dictionary of all available formatters"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        formatters[formatter().formats] = formatter()
    return formatters
