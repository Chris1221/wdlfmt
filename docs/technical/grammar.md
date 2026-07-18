# Grammar & ANTLR4

`wdlfmt` parses WDL using [ANTLR4](https://www.antlr.org/). The grammar lives in `wdlfmt/grammar/` and the generated Python files are committed to the repository so users don't need the ANTLR4 tool installed.

## Grammar files

| File | Purpose |
|------|---------|
| `wdlfmt/grammar/WdlV1Lexer.g4` | Lexer grammar — defines tokens (keywords, identifiers, literals, comments) |
| `wdlfmt/grammar/WdlV1Parser.g4` | Parser grammar — defines the WDL v1.0 syntax tree rules |
| `wdlfmt/grammar/WdlV1Lexer.py` | Generated Python lexer |
| `wdlfmt/grammar/WdlV1Parser.py` | Generated Python parser |
| `wdlfmt/grammar/WdlV1ParserVisitor.py` | Generated visitor base class |
| `wdlfmt/grammar/WdlV1ParserListener.py` | Generated listener base class |

## How the grammar is used

The lexer tokenises raw WDL text and routes tokens to three channels:

| Channel | Contents |
|---------|---------|
| 0 | Default — all meaningful tokens |
| 1 | Whitespace (ignored by parser) |
| 2 | Comments — extracted manually before parsing |

The parser consumes channel 0 tokens and builds a typed parse tree. Each grammar rule `foo` corresponds to a `FooContext` class in `WdlV1Parser.py`.

## Regenerating the grammar

You only need to regenerate if you modify a `.g4` file. You need Java and the ANTLR4 tool:

```sh
# Download the ANTLR4 jar (do this once)
curl -O https://www.antlr.org/download/antlr-4.12.0-complete.jar

# Regenerate from the grammar directory
cd wdlfmt/grammar
java -jar /path/to/antlr-4.12.0-complete.jar \
    -Dlanguage=Python3 \
    -visitor \
    WdlV1Lexer.g4 WdlV1Parser.g4
```

This overwrites `WdlV1Lexer.py`, `WdlV1Parser.py`, `WdlV1ParserVisitor.py`, and `WdlV1ParserListener.py`. Commit all four generated files.

!!! warning
    The generated files are large and contain no hand-written code. Do not edit them directly — changes will be overwritten on the next regeneration.

## Notable grammar extensions

The grammar in this repo extends the reference WDL v1.0 grammar with one addition:

**`Identifier EQUAL string` in `expression_placeholder_option`**

The original grammar's `SEPEQUAL` token matched only `sep=` (no spaces). Some real-world WDL files write `sep = '...'` (with spaces around `=`). The grammar was extended to handle this:

```antlr
expression_placeholder_option
  : BoolLiteral EQUAL string
  | SEPEQUAL string
  | Identifier EQUAL string   ← added
  | DEFAULTEQUAL expr
  ;
```

## When to regenerate

- You added or changed a lexer rule in `WdlV1Lexer.g4`
- You added or changed a parser rule in `WdlV1Parser.g4`
- You upgraded the ANTLR4 runtime version (match the jar version to `antlr4-python3-runtime` in `pyproject.toml`)

After regeneration, run the full test suite to check nothing regressed:

```sh
pixi run test
```
