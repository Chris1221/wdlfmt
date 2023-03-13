import logging


def init_logger(level="debug", file=None, name=None):
    """Initiate a logging instance for the model."""

    assert level.upper() in dir(logging), f"Invalid log level ({level})"

    if file is not None:
        logging.basicConfig(filename=file, level=level.upper())
    else:
        logging.basicConfig(level=level.upper())

    return logging.getLogger(name if name else __name__)


def get_raw_text(ctx):
    stream = ctx.start.getInputStream()

    start = ctx.start.start
    stop = ctx.stop.stop + 1

    return stream.strdata[start:stop] + "\n"


# def create_public_formatters_dict():
#     """Create a dictionary of all public formatters.

#     Public formatters are formatters that are used by default.
#     This has to be in a seperate module to avoid circular imports.
#     """
#     task_formatters = collect_task_formatters()
#     common_formatters = collect_common_formatters()

#     formatters = {**task_formatters, **common_formatters}

#     return formatters
