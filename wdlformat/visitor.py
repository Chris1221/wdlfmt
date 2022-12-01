from .grammar.WdlV1Lexer import WdlV1Lexer
from .grammar.WdlV1Parser import WdlV1Parser, ParserRuleContext
from .grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from antlr4 import CommonTokenStream, InputStream

from .utils import create_public_formatters_dict
from .formatters.common import CommentContext, flatten_tree_and_insert_comments


class WdlVisitor(WdlV1ParserVisitor):
    def __init__(self, input_stream):
        # Set up the formatters
        self.formatters = create_public_formatters_dict()

        # # Set up the listeners
        # for cls, formatter in self.formatters.items():
        #     setattr(
        #         self, f"visit{cls.__name__.replace('Context', '')}", self.baseVisitor
        #     )

        self.formatted = ""
        lexer = WdlV1Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        # tokens with a channel of 0 are the default channel
        # tokens with a channel of 1 are the hidden channel
        # tokens with a channel of 2 are the comments channel

        # This is hacky AF but can I change the channel of the tokens?
        # This doesn't actually work, maybe because it doesn't line up
        # with the parser?
        #
        # Anyway I think my options are either:
        #     1. Remove the comment channel entirely and regenerate the
        #        parser
        #     2. Record the start and end position of the comments and
        #        then insert them back in after the fact
        #
        # I want to try 1 before resorting to 2
        comment_tokens = []
        idxs = []
        stream.fill()
        for token in stream.tokens:
            if token.channel == 2:
                comment_tokens.append(token)
                idxs.append(token.tokenIndex)

        comment_ctx = [CommentContext(token) for token in comment_tokens]

        # stream.tokens = new_tokens

        # Attempt 2:
        # I'm going to create a context for each of the comments
        # on the fly and then add them to the tree

        # I can :
        #     1. flatten the tree to get the token index
        #     2. get the token index from each comment
        #     3. add them in the right place
        # Will I have to update the token index of the other tokens? Not sure

        parser = WdlV1Parser(stream)

        tree = parser.document()

        # Recusively flatten the tre and insert the comments
        tree = flatten_tree_and_insert_comments(tree, comment_ctx, idxs)
        sdfasd
        self.visit(tree)

    def __str__(self):
        return self.formatted

    def format(self, ctx):
        """Get the formatter for the current class"""
        return self.formatters[type(ctx)].format(ctx)

    def baseVisitor(self, ctx: ParserRuleContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitTask(self, ctx: WdlV1Parser.TaskContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitMeta_string(self, ctx: WdlV1Parser.Meta_stringContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)


def test():
    input = open("test/test_md5.wdl", "r").read()
    input_stream = InputStream(input)
    print(WdlVisitor(input_stream))
