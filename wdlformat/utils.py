import logging
import re
import difflib
import wdlformat.formatters


def init_logger(level="debug", file=None, name=None):
    """Initiate a logging instance for the model."""

    assert level.upper() in dir(logging), f"Invalid log level ({level})"

    if file is not None:
        logging.basicConfig(filename=file, level=level.upper())
    else:
        logging.basicConfig(level=level.upper())

    return logging.getLogger(name if name else __name__)


def get_raw_text(ctx):

    # Comments are just mocked up context objects so do not
    # have the convenience methods below
    if isinstance(ctx, wdlformat.formatters.common.CommentContext):
        return ctx.getText() + "\n"

    stream = ctx.start.getInputStream()

    start = ctx.start.start
    stop = ctx.stop.stop + 1

    return stream.strdata[start:stop] + "\n"


def assert_text_equal(original, formatted, check=True):
    """Assert that the actual content of a formatted string
    does not change."""

    if not check:
        return formatted

    original_text = get_raw_text(original)

    regex = re.compile("[^a-zA-Z]")

    original_raw = regex.sub("", original_text).split()
    formatted_raw = regex.sub("", formatted).split()

    if original_raw != formatted_raw:
        original_words = [i for i in re.split(regex, original_text) if i]
        formatted_words = [i for i in re.split(regex, formatted) if i]
        for diff in difflib.context_diff(original_words, formatted_words):
            print(diff)

        raise AssertionError(
            "Formatted text not identitical to original, see the above diff"
        )

    return formatted
