from .grammar.WdlV1Parser import WdlV1Parser
from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, input) -> str:
        pass


class VersionFormatter(Formatter):
    def format(self, input) -> str:
        return f"{input.VERSION().getText()} {input.ReleaseVersion().getText()}\n"


# Overall dictionary for storing formatters
# I don't know if there's a cleaner way to
# do this but it's not bad
formatters: dict = {WdlV1Parser.VersionContext: VersionFormatter()}
