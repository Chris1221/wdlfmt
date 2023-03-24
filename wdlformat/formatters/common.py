from ..grammar.WdlV1Parser import (
    WdlV1Parser,
    ParserRuleContext,
    ParseTreeListener,
    ParseTreeVisitor,
)
from abc import ABC, abstractmethod

from ..utils import init_logger

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
    def __init__(self):
        self.log = init_logger(name=__name__)

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


def subset_children(children, types):
    if isinstance(types, list):
        out = []
        for t in types:
            out += [i for i in children if isinstance(i, t)]
        return out
    else:
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
                    breakpoint()
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
                    breakpoint()
                    comment.top_level = toplevel
                    tree.children.insert(tree.children.index(child), comment)
                    found += [idx]
                    found_comments += [comment]
                    break

    return tree, found, found_comments


def get_position(node):
    if hasattr(node, "start"):
        return node.start.tokenIndex
    else:
        return node.symbol.tokenIndex


def flatten_context_tree(tree, flat=[]):
    for child in tree.children:
        if hasattr(child, "children"):
            flat.append(get_position(child))
            flat = flatten_context_tree(child)
        else:
            flat.append(get_position(child))

    return flat


def find_elm_with_given_index_in_tree(tree, idx):
    """Find the element with the given index in the tree"""

    # Prefer top-level elements, because this means
    # that the comment is before the first element
    # in the subtree
    if get_position(tree) == idx:
        return tree

    else:
        for child in tree.children:
            if hasattr(child, "children"):
                elm = find_elm_with_given_index_in_tree(child, idx)
                if elm:
                    return elm
            else:
                if get_position(child) == idx:
                    return child
    return None


def find_comment_neighbours(comment_idxs, all_idxs, tree):
    """Find the neighbour elements of a comment in the tree"""
    neighbours = []
    found = False
    for cidx in comment_idxs:
        for idx in all_idxs:
            if idx > cidx:
                neighbours.append(find_elm_with_given_index_in_tree(tree, idx))
                found = True
                break

        if not found:
            neighbours.append(find_elm_with_given_index_in_tree(tree, all_idxs[-1]))

    return neighbours


def insert_comment_into_tree(tree, comment, neighbour):
    """Find the neighbour in the tree and insert the comment
    at the same scope level"""

    if tree == neighbour:
        comment.top_level = "DocumentContext" in str(type(tree.parentCtx))
        tree.parentCtx.children.insert(tree.parentCtx.children.index(tree), comment)
        return tree.parentCtx

    else:
        if hasattr(tree, "children") and "Comment" not in str(type(tree)):
            for child in tree.children:
                if child == neighbour:
                    comment.top_level = "DocumentContext" in str(type(tree))
                    # breakpoint()
                    tree.children.insert(tree.children.index(child), comment)
                    return tree
                else:
                    child_index = tree.children.index(child)
                    child = insert_comment_into_tree(child, comment, neighbour)
                    tree.children[child_index] = child

        return tree


def insert_comments(tree, comments, comment_idxs):
    """Insert comments in the tree"""
    # Find the neighbour elements of the comments
    all_idxs = flatten_context_tree(tree)
    neighbours = find_comment_neighbours(comment_idxs, all_idxs, tree)

    # Insert the comments in the tree
    for comment, neighbour in zip(comments, neighbours):
        tree = insert_comment_into_tree(tree, comment, neighbour)

    return tree


def collect_formatters(only_public: bool = True):
    """Collect all the formatters for tasks"""
    formatters = {}
    for formatter in Formatter.__subclasses__():
        if only_public and not formatter.public:
            continue

        if isinstance(formatter().formats, list):
            for format in formatter().formats:
                formatters[str(format)] = formatter()
        else:
            formatters[str(formatter().formats)] = formatter()

    return formatters


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
    return {**collect_formatters()}
