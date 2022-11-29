import subprocess
from abc import ABC, abstractmethod
from tempfile import NamedTemporaryFile
from os import remove


class ShellFormatter(ABC):
    def __init__(self, command):
        self.command = command

        assert self.enabled, f"{self.__class__.__name__} is not enabled"

    @abstractmethod
    def format(self) -> str:
        """Format a file with a given formatter"""
        pass

    @property
    @abstractmethod
    def enabled(self):
        """Whether or not the formatter should be used by default"""
        pass


class ShfmtFormatter(ShellFormatter):
    enabled = True

    def format(self) -> str:
        try:
            with NamedTemporaryFile(delete=False) as tmpfile:
                tmpfile.write(self.command.encode("utf-8"))
                tmpfile.flush()  # necessary
                formatted = subprocess.check_output(["shfmt", tmpfile.name]).decode(
                    "utf-8"
                )
        finally:
            remove(tmpfile.name)

        return formatted
