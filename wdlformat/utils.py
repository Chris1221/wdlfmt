from .formatters.task import collect_task_formatters
from .formatters.common import collect_common_formatters


def create_public_formatters_dict():
    """Create a dictionary of all public formatters.

    Public formatters are formatters that are used by default.
    This has to be in a seperate module to avoid circular imports.
    """
    task_formatters = collect_task_formatters()
    common_formatters = collect_common_formatters()

    formatters = {**task_formatters, **common_formatters}

    return formatters
