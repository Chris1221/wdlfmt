from ..grammar.WdlV1Parser import (
    WdlV1Parser,
    ParserRuleContext,
    ParseTreeListener,
    ParseTreeVisitor,
)
from abc import ABC, abstractmethod

DEBUG = True


class CommentContext(ParserRuleContext):
    __slots__ = "parser"

    def __init__(self, token):
        super().__init__(None, -1)
        self.token = token

    def getRuleIndex(self):
        return WdlV1Parser.RULE_task

    def getText(self):
        return self.token.text

    def enterRule(self, listener: ParseTreeListener):
        if hasattr(listener, "enterTask"):
            listener.enterTask(self)

    def exitRule(self, listener: ParseTreeListener):
        if hasattr(listener, "exitTask"):
            listener.exitTask(self)

    def accept(self, visitor: ParseTreeVisitor):
        if hasattr(visitor, "visitComment"):
            return visitor.visitComment(self)
        else:
            return visitor.visitChildren(self)


class Formatter(ABC):
    @abstractmethod
    def format(self, input: ParserRuleContext, indent: int = 0) -> str:
        """Logic for formatting the input"""
        pass

    @property
    @abstractmethod
    def formats(self):
        """Class of the input to format"""
        pass

    @property
    @abstractmethod
    def public(self):
        """Whether or not the formatter should be used by default"""
        pass


def collect_common_formatters():
    """Collect all the formatters for tasks"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        if formatter().public:
            formatters[formatter().formats] = formatter()
    return formatters


def subset_children(children, types):
    return [i for i in children if isinstance(i, types)]


def indent_text(text, level=0, spaces=4):
    return "".join([f"{' '*spaces*level}{line}" for line in text.splitlines(True)])


def create_formatters_dict():
    """Create a dictionary of all formatters"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        formatters[formatter().formats] = formatter()
    return formatters


def flatten_tree_and_insert_comments(
    tree, comments, idxs, found=[], found_comments=[], toplevel=True
):
    """Flatten the tree and insert comments in the right place"""

    print(f"Initial found: {found}")

    # If we've already found the comment, don't do anything
    for f in found:
        if f in idxs:
            idxs.remove(f)

    for f in found_comments:
        if f in comments:
            comments.remove(f)

    for idx, comment in zip(idxs, comments):
        print("Checking idx: ", idx)
        # set = False

        # If we've already found the comment, don't do anything

        # if idx == 18:
        #     breakpoint()

        for child in tree.children:

            # if set:
            #     break

            if idx in found:
                continue

            # If the child is a comment, skip it
            # I know... this is a hack
            if isinstance(child, CommentContext) or "Comment" in str(type(child)):
                continue

            if hasattr(child, "children"):
                # Check if the comment is in the children
                tkn_index = child.start.tokenIndex

                if tkn_index >= idx:
                    # If it is, insert the comment
                    comment.top_level = toplevel
                    tree.children.insert(tree.children.index(child), comment)
                    found.append(idx)
                    found_comments.append(comment)
                    break
                else:
                    # If it isn't, recurse
                    nfound = len(found)
                    child, found, found_comments = flatten_tree_and_insert_comments(
                        child, comments, idxs, found, found_comments, False
                    )
                    if len(found) > nfound:
                        print(f"Found comment: {found[-1]}")
                        # set = True
                        tree.children[tree.children.index(child)] = child
                        break

            else:
                tkn_idx = child.symbol.tokenIndex
                if tkn_idx >= idx:
                    print(f"Adding at {tkn_idx} {comment}")
                    comment.top_level = toplevel
                    tree.children.insert(tree.children.index(child), comment)
                    found += [idx]
                    found_comments += [comment]
                    break

    return tree, found, found_comments
