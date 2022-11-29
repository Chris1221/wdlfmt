from .formatters.task import collect_task_formatters
from .formatters.common import collect_common_formatters


def create_public_formatters_dict():
    """Create a dictionary of all public formatters"""
    task_formatters = collect_task_formatters()
    common_formatters = collect_common_formatters()

    formatters = {**task_formatters, **common_formatters}

    return formatters
