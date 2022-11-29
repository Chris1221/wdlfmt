from .grammar.WdlV1Lexer import WdlV1Lexer
from .grammar.WdlV1Parser import WdlV1Parser, ParserRuleContext
from .grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from antlr4 import CommonTokenStream, InputStream

from .utils import create_public_formatters_dict


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
        # new_tokens = []
        # stream.fill()
        # for token in stream.tokens:
        #     if token.channel == 2:
        #         token.channel = 1

        #     new_tokens.append(token)

        # stream.tokens = new_tokens

        parser = WdlV1Parser(stream)
        tree = parser.document()
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

    def visitMeta_element(self, ctx: WdlV1Parser.Meta_elementContext):
        asdfasd
        return self.visitChildren(ctx)


def test():
    input = open("test/test_md5.wdl", "r").read()
    input_stream = InputStream(input)
    print(WdlVisitor(input_stream))
