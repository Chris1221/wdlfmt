# Architecture

`wdlfmt` is a pipeline with five stages: parse, extract comments, insert comments, visit, and check.

## Pipeline overview

```
WDL source text
      │
      ▼
┌─────────────────────────────────┐
│  ANTLR4 Lexer (WdlV1Lexer)     │
│  Tokenises the input stream     │
│  Comments → channel 2           │
└──────────┬──────────────────────┘
           │ token stream
           ▼
┌─────────────────────────────────┐
│  Comment extraction             │
│  Scan channel 2 tokens →        │
│  list of CommentContext nodes   │
└──────────┬──────────────────────┘
           │ comment nodes + token indices
           ▼
┌─────────────────────────────────┐
│  ANTLR4 Parser (WdlV1Parser)   │
│  Builds typed parse tree        │
│  (TaskContext, WorkflowContext, │
│   StructContext, …)             │
└──────────┬──────────────────────┘
           │ parse tree
           ▼
┌─────────────────────────────────┐
│  Comment injection              │
│  insert_comments() places each  │
│  CommentContext before its      │
│  nearest following token node   │
└──────────┬──────────────────────┘
           │ augmented parse tree
           ▼
┌─────────────────────────────────┐
│  WdlVisitor walk                │
│  Visits top-level nodes;        │
│  delegates to Formatter         │
│  registry for each context type │
└──────────┬──────────────────────┘
           │ formatted WDL string
           ▼
┌─────────────────────────────────┐
│  StyleChecker                   │
│  Regex checks on formatted text │
│  Emits checklist to stderr      │
└─────────────────────────────────┘
```

## Key design decisions

### Comment channel

ANTLR4 routes tokens to named channels. The WDL lexer puts comments (`#`) on channel 2, which is invisible to the parser. `wdlfmt` extracts them from the raw token stream *before* parsing, stores them as `CommentContext` nodes with their original token indices, then re-inserts them into the parse tree in the correct position based on token index proximity.

This makes formatting **lossless** — no comments are dropped.

### Formatter registry

Rather than a monolithic visitor method per context type, each WDL element has its own `Formatter` subclass. The registry is built automatically at import time by inspecting all `Formatter` subclasses (see [Adding Formatters](formatters.md)). This makes it easy to add or modify formatting for individual WDL constructs without touching the visitor.

### Shell script formatting

WDL `command <<<` blocks contain shell script. `wdlfmt` delegates shell formatting to [`shfmt`](https://github.com/mvdan/sh), bundled via `shfmt-py`. Because WDL interpolation expressions (`~{...}`) are not valid shell syntax, they are replaced with safe `WDLFMT_EXPRESSION_PLACEHOLDER_N_` tokens before passing the block to `shfmt`, then restored afterwards.

### Style checker decoupling

`StyleChecker` operates on the final formatted string using regex, with no re-parsing. This keeps it fast and independent of the formatter internals — it can be used standalone on any already-formatted WDL text.
