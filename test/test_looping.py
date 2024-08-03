# There's a weird bug right now where WDLFMT works fine
# if you run each one on a seperate thread, but has weirdly
# deterministic errors if you run it all togheter.
#
# I suspect that this is due to some kind of memory
# contamination changing how ANTLR4 is parsing the
# documents but I don't know for sure. Here are my attempts
# to figure it out by manually reconstructing the process of
# building the tree and seeing if it changes.

import glob

from antlr4 import CommonTokenStream, InputStream

from wdlfmt.formatters import struct, task, workflow
from wdlfmt.formatters.common import CommentContext, collect_formatters, insert_comments
from wdlfmt.grammar.WdlV1Lexer import WdlV1Lexer
from wdlfmt.grammar.WdlV1Parser import ParserRuleContext, WdlV1Parser
from wdlfmt.grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from wdlfmt.utils import assert_text_equal, get_raw_text, init_logger
from wdlfmt.visitor import WdlVisitor


def test_looping():
    input_stream = InputStream(open("test/biowdl_tasks/common.wdl").read())
    working_visitor = WdlVisitor(input_stream)
    common_formatted = str(working_visitor)

    # Now let's go over a bunch of them and break it
    biowdl_tasks = glob.glob("test/biowdl_tasks/*.wdl")

    # Remove hmftools, there's a syntax error in that one
    biowdl_tasks = [task for task in biowdl_tasks if "hmftools" not in task]

    for task in biowdl_tasks:
        input_stream = InputStream(open(task).read())
        visitor = WdlVisitor(input_stream)
