from .grammar.WdlV1Lexer import WdlV1Lexer
from .grammar.WdlV1Parser import WdlV1Parser, ParserRuleContext
from .grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from antlr4 import CommonTokenStream, InputStream

# from .utils import create_public_formatters_dict
from wdlformat.formatters.common import (
    CommentContext,
    insert_comments,
    collect_common_formatters,
)
from wdlformat.formatters.task import collect_task_formatters
from wdlformat.formatters.workflow import collect_workflow_formatters
from wdlformat.formatters.struct import collect_struct_formatters

from .utils import get_raw_text, init_logger, assert_text_equal

from typing import List


def create_public_formatters_dict():
    """Create a dictionary of all public formatters.

    Public formatters are "top-level" meaning they exist
    outside a task or workflow context. A "public" versus
    "private" dictinction is used to allow individual
    formatters discretion over how they wish to treat
    their elements. This also allows us to consistently
    set indentation levels for all formatters without the
    need to pass around a context object.

    Returns:
        dict: Dictionary of all public formatters
    """
    task_formatters = collect_task_formatters()
    common_formatters = collect_common_formatters()
    workflow_formatters = collect_workflow_formatters()
    struct_formatters = collect_struct_formatters()

    formatters = {
        **task_formatters,
        **common_formatters,
        **workflow_formatters,
        **struct_formatters,
    }

    return formatters


class WdlVisitor(WdlV1ParserVisitor):
    def __init__(self, input_stream):
        # Set up the formatters
        self.formatters = create_public_formatters_dict()

        # Set up the listeners and parse the
        # token stream from the lexer
        self.formatted = ""
        lexer = WdlV1Lexer(input_stream)
        stream = CommonTokenStream(lexer)

        # The parser has three channels:
        # 0: The default channel
        # 1: The whitespace channel
        # 2: The comments channel

        # We want to work with the comments channel
        # but cannot directly parse it, so we read in
        # all of the tokens directly from the lexer
        # and thread them into the tree behind their
        # nearest top-level node.

        # First we get all the tokens from the lexer
        # in the comments channel and record their
        # indices
        comment_tokens = []
        idxs = []
        stream.fill()
        for token in stream.tokens:
            if token.channel == 2:
                comment_tokens.append(token)
                idxs.append(token.tokenIndex)

        # The CommentContext is a mocked up context
        # class that we use to insert the comments. It has
        # manually set .getText() methods that return the
        # comment text.
        comment_ctx = [CommentContext(token) for token in comment_tokens]
        parser = WdlV1Parser(stream)

        # Parse the input and recusively visit the tree
        # to add the comment nodes
        tree = parser.document()
        tree = insert_comments(tree, comment_ctx, idxs)

        self.log = init_logger(name=__name__)

        # Visit the tree and format the WDL, filling in the
        # self.formatted string with the formatted WDL
        self.visit(tree)

        assert_text_equal(tree, self.formatted)

    def __str__(self):
        """The print method for the visitor will return the
        formatted WDL"""
        return self.formatted

    def format(self, ctx):
        """Get the formatter for the current class"""
        self.log.debug(f"Formatting {ctx.__repr__()}")
        if isinstance(ctx, CommentContext):
            check = False
        else:
            check = True

        try:
            return assert_text_equal(
                ctx, self.formatters[str(type(ctx))].format(ctx), check
            )
        except KeyError:
            self.log.warn(f"Missing formatter for: {ctx.__repr__()}")
            self.log.debug(f"Writing the following instead:\n{get_raw_text(ctx)}\n")
            return get_raw_text(ctx)
        except AssertionError as e:
            self.log.error("Error formatting this block. See the diff above")
            raise e

    def visitVersion(self, ctx: WdlV1Parser.VersionContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def baseVisitor(self, ctx: ParserRuleContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitTask(self, ctx: WdlV1Parser.TaskContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitWorkflow(self, ctx: WdlV1Parser.WorkflowContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitComment(self, ctx: CommentContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitStruct(self, ctx: WdlV1Parser.StructContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)


def format_wdl(
    files: List[str] = "test/test_md5.wdl",
    in_place: bool = False,
):
    """Format a WDL file

    Args:
        files (List[str]): List of WDL files to format (can also be a string)
        in_place (bool, optional): Whether to edit the file in place. Defaults to False.
    """
    if isinstance(files, str):
        files = [files]

    for file in files:
        with open(file, "r") as f:
            input_stream = InputStream(f.read())

        visitor = WdlVisitor(input_stream)

        if in_place:
            with open(file, "w") as f:
                f.write(str(visitor))
        else:
            print(str(visitor))
