from .grammar.WdlV1Lexer import WdlV1Lexer
from .grammar.WdlV1Parser import WdlV1Parser
from .grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from antlr4 import CommonTokenStream, InputStream
from abc import ABC, abstractmethod
from .formatters import create_formatters_dict


class WdlVisitor(WdlV1ParserVisitor):
    def __init__(self, input_stream):
        # Set up the formatters
        self.formatters = create_formatters_dict()

        self.formatted = ""
        lexer = WdlV1Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = WdlV1Parser(stream)
        tree = parser.document()
        self.visit(tree)

        # I could also:
        #   use setattr to set the visit methods
        #   programatically, but this would require
        #   that all of the logic would be held entirely
        #   in the formatters.
        #
        #   I don't know yet if I need different logic
        #   for the visitor that would be seperate from the
        #   formatters. It's easy enough to change over after
        #   wards though, just looping over all the
        #   methods that start with `visit` and replacing
        #   them with the visitor below

    def __str__(self):
        return self.formatted

    def format(self, ctx):
        """Get the formatter for the current class"""
        return self.formatters[type(ctx)].format(ctx)

    def visitVersion(self, ctx: WdlV1Parser.VersionContext):
        self.formatted = self.format(ctx)
        return self.visitChildren(ctx)


def test():
    input = open("test/test_md5.wdl", "r").read()
    input_stream = InputStream(input)
    print(WdlVisitor(input_stream))
