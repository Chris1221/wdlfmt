# Visitor Pattern

`wdlfmt` uses the ANTLR4 visitor pattern to walk the WDL parse tree and produce formatted output.

## Why the visitor pattern?

A WDL file is a tree of typed context nodes — `DocumentContext` at the root, with `TaskContext`, `WorkflowContext`, and `StructContext` children, each of which has its own subtree of inputs, outputs, commands, runtime blocks, and so on.

The visitor pattern separates the *traversal logic* (which nodes to visit, in what order) from the *formatting logic* (what to emit for each node type). This means:

- Adding support for a new WDL construct means adding a new `Formatter` subclass — the visitor itself doesn't change.
- Each formatter can be tested in isolation.
- The visitor only needs to know about top-level constructs; sub-element formatting is handled recursively within each formatter.

## `WdlVisitor`

`WdlVisitor` (in `wdlfmt/visitor.py`) extends ANTLR4's generated `WdlV1ParserVisitor` and accumulates formatted output in `self.formatted`.

```python
class WdlVisitor(WdlV1ParserVisitor):
    def visitTask(self, ctx: WdlV1Parser.TaskContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitWorkflow(self, ctx: WdlV1Parser.WorkflowContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitStruct(self, ctx: WdlV1Parser.StructContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)

    def visitComment(self, ctx: CommentContext):
        self.formatted += self.format(ctx)
        return self.visitChildren(ctx)
```

Each `visitX` method calls `self.format(ctx)`, which looks up the appropriate `Formatter` from the registry by the context's type string, delegates formatting to it, and appends the result to `self.formatted`.

## Comment injection

Comments are extracted from ANTLR token channel 2 before parsing, then re-inserted into the parse tree as `CommentContext` nodes by `insert_comments()` in `wdlfmt/formatters/common.py`.

The algorithm:

1. **`flatten_context_tree(tree)`** — collect the token index of every node in the parse tree into a flat sorted list.
2. **`find_comment_neighbours(comment_idxs, all_idxs, tree)`** — for each comment token index, find the first parse-tree node whose token index is *greater than* the comment's. That node is the comment's "neighbour" (the node it precedes).
3. **`insert_comment_into_tree(tree, comment, neighbour)`** — traverse the tree to find the neighbour node, then insert the `CommentContext` immediately before it in the parent's children list. The `top_level` flag is set based on whether the parent is a `DocumentContext`, controlling indentation in the formatter.

## `CommentContext`

`CommentContext` is a lightweight mock of `ParserRuleContext` that wraps a single ANTLR token. It overrides `getText()` to return the comment text and `accept()` to call `visitor.visitComment()`. This lets comments flow through the same visitor machinery as real parse-tree nodes.

```python
class CommentContext(ParserRuleContext):
    def __init__(self, token):
        super().__init__(None, -1)
        self.token = token

    def getText(self):
        return self.token.text

    def accept(self, visitor):
        if hasattr(visitor, "visitComment"):
            return visitor.visitComment(self)
```

## Formatter registry

`collect_formatters()` builds a dict mapping `str(ContextClass)` → `Formatter()` by inspecting all subclasses of `Formatter`. This is called once when `WdlVisitor` is instantiated:

```python
self.formatters = {**collect_formatters()}
```

When `self.format(ctx)` is called, it looks up `str(type(ctx))` in this dict and delegates:

```python
formatted = self.formatters[str(type(ctx))].format(ctx)
```

See [Adding Formatters](formatters.md) for how to extend this registry.
