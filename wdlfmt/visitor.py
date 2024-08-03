import gc
from typing import List

from antlr4 import CommonTokenStream, InputStream

# This import must come before common
# for the dependency resolution order
# to make all subclasses visible.
from wdlfmt.formatters import struct, task, workflow
from wdlfmt.formatters.common import CommentContext, collect_formatters, insert_comments

from .grammar.WdlV1Lexer import WdlV1Lexer
from .grammar.WdlV1Parser import ParserRuleContext, WdlV1Parser
from .grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from .utils import assert_text_equal, get_raw_text, init_logger


class WdlVisitor(WdlV1ParserVisitor):
    def __init__(self, input_stream):
        # Set up the formatters
        self.formatters = {**collect_formatters()}

        # Set up the listeners and parse the
        # token stream from the lexer
        self.formatted = ""
        lexer = WdlV1Lexer(input_stream)

        lexer.atn.decisionToState = []
        lexer.decisionsToDFA = []
        lexer.reset()

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
        parser.sharedContextCache.cache.clear()
        # parser.atn.decisionToState = []
        # parser.decisionsToDFA = []

        # Parse the input and recusively visit the tree
        # to add the comment nodes
        self.tree = parser.document()
        self.tree = insert_comments(self.tree, comment_ctx, idxs)
        self.log = init_logger(name=__name__)

        parser.reset()
        lexer.reset()
        parser.sharedContextCache.cache.clear()

    def __str__(self):
        """The print method for the visitor will return the
        formatted WDL"""
        self.visit(self.tree)
        return self.formatted

    def format(self, ctx):
        """Get the formatter for the current class"""
        self.log.debug(f"Formatting {ctx.__repr__()}")
        if isinstance(ctx, CommentContext):
            check = False
        else:
            check = True

        formatted = self.formatters[str(type(ctx))].format(ctx)

        # Now let's check to see if the formatting was applied correctly.
        # Step 1: Remove any comments
        lines = formatted.split("\n")
        lines = "\n".join([line for line in lines if not line.startswith("#")])

        assert_text_equal(ctx, lines, check)
        return formatted

        # except KeyError:
        #     self.log.warn(f"Missing formatter for: {ctx.__repr__()}")
        #     self.log.debug(f"Writing the following instead:\n{get_raw_text(ctx)}\n")
        #     return get_raw_text(ctx)
        # except AssertionError as e:
        #     self.log.error("Error formatting this block. See the diff above")
        #     raise e

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


def add_footer(formatted):
    """Add a footer to the formatted WDL"""
    # Add the date and time and a link to the GIthub repo
    import datetime

    footer = f"# Formatted by wdlfmt (https://github.com/Chris1221/wdlfmt) on {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}\n"

    # Let's check if there's already a footer
    # and if so replace it
    last_line = formatted.split("\n")[-1]
    second_to_last_line = formatted.split("\n")[-2]
    if last_line.startswith("# Formatted by wdlfmt"):
        formatted = "\n\n".join(formatted.split("\n")[:-1])

    elif second_to_last_line.startswith("# Formatted by wdlfmt"):
        formatted = "\n\n".join(formatted.split("\n")[:-2])

    formatted += footer
    return formatted


def format_wdl(
    files: List[str] = "test/test_md5.wdl", in_place: bool = False, return_object=False
):
    """Format a WDL file

    Args:
        files (List[str]): List of WDL files to format (can also be a string)
        in_place (bool, optional): Whether to edit the file in place. Defaults to False.
    """
    if isinstance(files, str):
        files = [files]

    logger = init_logger(name=__name__)

    if return_object:
        formatted_wdls = []

    for file in files:
        with open(file, "r") as f:
            input_stream = InputStream(f.read())

        try:
            formatted = str(WdlVisitor(input_stream))
        except Exception as e:
            logger.error(f"Could not format {file}, see below for error message.")
            raise e

        formatted = add_footer(formatted)

        if in_place:
            with open(file, "w") as f:
                f.write(add_footer(formatted))
        else:
            if not return_object:
                print(add_footer(formatted))
            else:
                formatted_wdls.append(formatted)

    if return_object:
        if len(formatted_wdls) == 0:
            raise ValueError("Failed to return any data")
        elif len(formatted_wdls) == 1:
            return formatted_wdls[0]
        else:
            return formatted_wdls


def format_wdl_str(wdl: str):
    """Returns the formatted version of a WDL passed in as a string."""
    input_stream = InputStream(wdl)
    visitor = WdlVisitor(input_stream)
    return str(visitor)
