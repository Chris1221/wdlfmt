from .grammar.WdlV1Lexer import WdlV1Lexer
from .grammar.WdlV1Parser import WdlV1Parser
from .grammar.WdlV1ParserVisitor import WdlV1ParserVisitor
from antlr4 import CommonTokenStream, InputStream
from abc import ABC, abstractmethod
from .formatters import formatters


class WdlVisitor(WdlV1ParserVisitor):
    def __init__(self, input_stream):
        # Set up the formatters
        self.formatters = formatters

        self.formatted = ""
        lexer = WdlV1Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = WdlV1Parser(stream)
        tree = parser.document()
        self.visit(tree)

    def __str__(self):
        return self.formatted

    def lookupFormatter(self, ctx):
        """Get the formatter for the current class"""
        return self.formatters[type(ctx)]

    def visitDocument(self, ctx):
        return self.visitChildren(ctx)

    def visitVersion(self, ctx: WdlV1Parser.VersionContext):
        self.formatted = self.lookupFormatter(ctx).format(ctx)
        return self.visitChildren(ctx)


def test():
    input = open("test/test_md5.wdl", "r").read()
    input_stream = InputStream(input)
    print(WdlVisitor(input_stream))