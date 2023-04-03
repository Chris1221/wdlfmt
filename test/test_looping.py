# There's a weird bug right now where WDLFMT works fine
# if you run each one on a seperate thread, but has weirdly
# deterministic errors if you run it all togheter.
#
# I suspect that this is due to some kind of memory
# contamination changing how ANTLR4 is parsing the
# documents but I don't know for sure. Here are my attempts
# to figure it out by manually reconstructing the process of
# building the tree and seeing if it changes.

from wdlfmt.grammar.WdlV1Lexer import WdlV1Lexer
from wdlfmt.grammar.WdlV1Parser import WdlV1Parser, ParserRuleContext
from wdlfmt.grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from antlr4 import CommonTokenStream, InputStream
from wdlfmt.formatters import task, workflow, struct
from wdlfmt.formatters.common import (
    CommentContext,
    insert_comments,
    collect_formatters,
)
from wdlfmt.utils import get_raw_text, init_logger, assert_text_equal
from wdlfmt.visitor import WdlVisitor
import glob


def test_looping():
    input_stream = InputStream(open("test/biowdl_tasks/common.wdl").read())
    working_visitor = WdlVisitor(input_stream)
    common_formatted = str(working_visitor)

    # Now let's go over a bunch of them and break it
    biowdl_tasks = glob.glob("test/biowdl_tasks/*.wdl")

    for task in biowdl_tasks:
        input_stream = InputStream(open(task).read())
        visitor = WdlVisitor(input_stream)

        try:
            formatted = str(visitor)
        except AssertionError:
            if task == "test/biowdl_tasks/common.wdl":
                failed_tree = visitor
                break

    assert formatted
