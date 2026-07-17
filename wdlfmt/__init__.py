from . import formatters  # noqa: F401
from .visitor import format_wdl, format_wdl_str  # noqa: F401
from .checker import StyleChecker, CheckResult, Status  # noqa: F401


def check_style(wdl: str) -> list:
    """Return a list of CheckResult for the given formatted WDL string."""
    return StyleChecker(wdl).run_all()
