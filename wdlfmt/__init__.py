from . import formatters
from .visitor import format_wdl, format_wdl_str
from .checker import StyleChecker, CheckResult, Status


def check_style(wdl: str) -> list:
    """Return a list of CheckResult for the given formatted WDL string."""
    return StyleChecker(wdl).run_all()
