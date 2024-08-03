import re
import subprocess
from abc import ABC, abstractmethod
from os import remove
from tempfile import NamedTemporaryFile


class ShellFormatter(ABC):
    def __init__(self, command, bin="shfmt"):
        self.command = command
        self.bin = bin

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

    def generate_placeholder(self):
        placeholder = f"WDLFMT_EXPRESSION_PLACEHOLDER_{self.placeholder_n}_"
        self.placeholder_n += 1
        return placeholder

    def find_and_replace_WDL_expressions(self, cmd):
        """Replaces ~ expressions with non-shell syntax with placeholders"""
        start_idxs = [match.start() for match in re.finditer("~{", cmd)]
        self.placeholder_n = 0
        self.placeholder_dict = {}

        # Begin at the start index and search forward until a match is found
        placeholders = {"starts": start_idxs, "stops": []}
        for starts in start_idxs:
            offset = 1
            for char in cmd[starts:]:
                if char == "}":
                    placeholders["stops"].append(starts + offset)
                    break
                else:
                    offset += 1

        assert len(placeholders["starts"]) == len(placeholders["stops"])

        expressions = []
        for p in range(len(placeholders["starts"])):
            start, stop = placeholders["starts"][p], placeholders["stops"][p]
            expressions.append(cmd[start:stop])

        for exp in expressions:
            placeholder = self.generate_placeholder()
            cmd = cmd.replace(exp, placeholder, 1)
            self.placeholder_dict[placeholder] = exp

        # Now replace the
        return cmd

    def restore_from_placeholders(self, cmd):
        """Put the original WDL expressions back"""

        for placeholder, exp in self.placeholder_dict.items():
            cmd = cmd.replace(placeholder, exp)

        return cmd

    def format(self) -> str:
        cmd = self.command
        cmd_sub = self.find_and_replace_WDL_expressions(cmd)
        try:
            with NamedTemporaryFile(delete=False) as tmpfile:
                tmpfile.write(cmd_sub.encode("utf-8"))
                tmpfile.flush()  # necessary
                formatted = subprocess.check_output([self.bin, tmpfile.name]).decode(
                    "utf-8"
                )
        finally:
            remove(tmpfile.name)

        restored = self.restore_from_placeholders(formatted)

        return restored
