"""BioWDL style guide compliance checker.

Runs on formatted WDL text (no re-parsing) and produces a per-rule report.
Reference: https://biowdl.github.io/styleGuidelines.html
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass
class CheckResult:
    rule: str
    status: Status
    details: str = ""


# ── helpers ──────────────────────────────────────────────────────────────────

def _is_upper_camel(name: str) -> bool:
    return bool(re.match(r"^[A-Z][a-zA-Z0-9]*$", name))


def _is_lower_camel(name: str) -> bool:
    return bool(re.match(r"^[a-z][a-zA-Z0-9]*$", name))


def _extract_command_blocks(text: str) -> list[str]:
    """Return the contents of every command <<< ... >>> block."""
    return re.findall(r"command\s*<<<(.*?)>>>", text, re.DOTALL)


def _task_names(text: str) -> list[str]:
    return re.findall(r"\btask\s+(\w+)\s*\{", text)


def _workflow_names(text: str) -> list[str]:
    return re.findall(r"\bworkflow\s+(\w+)\s*\{", text)


def _struct_names(text: str) -> list[str]:
    return re.findall(r"\bstruct\s+(\w+)\s*\{", text)


# ── checker ───────────────────────────────────────────────────────────────────

class StyleChecker:
    def __init__(self, formatted: str):
        self.text = formatted
        self.lines = formatted.splitlines()

    # -- formatter-guaranteed checks (always pass after wdlfmt) ---------------

    def check_indentation(self) -> CheckResult:
        return CheckResult(
            rule="4-space indentation",
            status=Status.PASS,
            details="enforced by wdlfmt",
        )

    def check_heredoc_syntax(self) -> CheckResult:
        return CheckResult(
            rule="Heredoc (<<<) command syntax",
            status=Status.PASS,
            details="enforced by wdlfmt",
        )

    def check_double_quotes(self) -> CheckResult:
        return CheckResult(
            rule="Double-quote string literals",
            status=Status.PASS,
            details="enforced by wdlfmt",
        )

    def check_operator_spacing(self) -> CheckResult:
        return CheckResult(
            rule="Spaces around = operator",
            status=Status.PASS,
            details="enforced by wdlfmt",
        )

    # -- content checks -------------------------------------------------------

    def check_line_length(self) -> CheckResult:
        offenders = [i + 1 for i, line in enumerate(self.lines) if len(line) > 100]
        if offenders:
            sample = ", ".join(str(n) for n in offenders[:5])
            suffix = f" (+{len(offenders)-5} more)" if len(offenders) > 5 else ""
            return CheckResult(
                rule="Line length ≤ 100 chars",
                status=Status.FAIL,
                details=f"{len(offenders)} line(s) exceed 100 chars: {sample}{suffix}",
            )
        return CheckResult(rule="Line length ≤ 100 chars", status=Status.PASS)

    def check_task_naming(self) -> CheckResult:
        bad = [n for n in _task_names(self.text) if not _is_upper_camel(n)]
        if bad:
            return CheckResult(
                rule="Task names are UpperCamelCase",
                status=Status.FAIL,
                details=f"Non-conforming: {', '.join(bad)}",
            )
        return CheckResult(rule="Task names are UpperCamelCase", status=Status.PASS)

    def check_workflow_naming(self) -> CheckResult:
        bad = [n for n in _workflow_names(self.text) if not _is_upper_camel(n)]
        if bad:
            return CheckResult(
                rule="Workflow names are UpperCamelCase",
                status=Status.FAIL,
                details=f"Non-conforming: {', '.join(bad)}",
            )
        return CheckResult(rule="Workflow names are UpperCamelCase", status=Status.PASS)

    def check_struct_naming(self) -> CheckResult:
        bad = [n for n in _struct_names(self.text) if not _is_upper_camel(n)]
        if bad:
            return CheckResult(
                rule="Struct names are UpperCamelCase",
                status=Status.FAIL,
                details=f"Non-conforming: {', '.join(bad)}",
            )
        return CheckResult(rule="Struct names are UpperCamelCase", status=Status.PASS)

    def check_call_aliases(self) -> CheckResult:
        """Warn for calls without an 'as' alias; fail if any alias is not lowerCamelCase."""
        # calls with an alias
        aliased = re.findall(r"\bcall\s+\S+\s+as\s+(\w+)", self.text)
        bad_case = [a for a in aliased if not _is_lower_camel(a)]

        # calls without any alias (call X { or call X\n{)
        all_calls = re.findall(r"\bcall\s+(\S+)", self.text)
        aliased_calls = re.findall(r"\bcall\s+(\S+)\s+as\s+\w+", self.text)
        missing_alias = [c for c in all_calls if c not in aliased_calls]

        if bad_case:
            return CheckResult(
                rule="Call aliases are lowerCamelCase",
                status=Status.FAIL,
                details=f"Non-conforming aliases: {', '.join(bad_case)}",
            )
        if missing_alias:
            return CheckResult(
                rule="Call aliases are lowerCamelCase",
                status=Status.WARN,
                details=f"Calls missing 'as' alias: {', '.join(missing_alias)}",
            )
        return CheckResult(rule="Call aliases are lowerCamelCase", status=Status.PASS)

    def check_set_pipefail(self) -> CheckResult:
        """Warn for command blocks with multiple commands but no set -e -o pipefail."""
        blocks = _extract_command_blocks(self.text)
        missing = []
        for i, block in enumerate(blocks):
            # Only care if there are multiple non-trivial command lines
            cmd_lines = [
                ln.strip() for ln in block.splitlines()
                if ln.strip() and not ln.strip().startswith("#")
            ]
            if len(cmd_lines) > 1 and "set -e -o pipefail" not in block:
                # Try to find what task this belongs to (rough heuristic)
                missing.append(f"block {i + 1}")

        if missing:
            return CheckResult(
                rule="set -e -o pipefail in multi-command blocks",
                status=Status.WARN,
                details=f"Missing in: {', '.join(missing)}",
            )
        return CheckResult(rule="set -e -o pipefail in multi-command blocks", status=Status.PASS)

    def check_parameter_meta(self) -> CheckResult:
        """Warn for tasks/workflows that have no parameter_meta block."""
        missing = []
        # Find each task/workflow block and check for parameter_meta inside it
        for pattern, kind in [(r"\btask\s+(\w+)\s*\{", "task"), (r"\bworkflow\s+(\w+)\s*\{", "workflow")]:
            for m in re.finditer(pattern, self.text):
                name = m.group(1)
                brace_pos = self.text.index("{", m.start())
                depth = 0
                block_end = brace_pos
                for i, ch in enumerate(self.text[brace_pos:], start=brace_pos):
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            block_end = i
                            break
                block_text = self.text[brace_pos:block_end]
                if "parameter_meta" not in block_text:
                    missing.append(f"{kind} '{name}'")

        if missing:
            return CheckResult(
                rule="parameter_meta section present",
                status=Status.WARN,
                details=f"Missing in: {', '.join(missing)}",
            )
        return CheckResult(rule="parameter_meta section present", status=Status.PASS)

    def check_docker_runtime(self) -> CheckResult:
        """Warn for runtime blocks that have no docker: entry."""
        runtime_blocks = re.findall(r"\bruntime\s*\{([^}]*)\}", self.text, re.DOTALL)
        missing_count = sum(1 for b in runtime_blocks if "docker" not in b)
        if missing_count:
            return CheckResult(
                rule="docker defined in runtime blocks",
                status=Status.WARN,
                details=f"{missing_count} runtime block(s) missing 'docker'",
            )
        if not runtime_blocks:
            return CheckResult(
                rule="docker defined in runtime blocks",
                status=Status.WARN,
                details="No runtime blocks found",
            )
        return CheckResult(rule="docker defined in runtime blocks", status=Status.PASS)

    # -- run all ---------------------------------------------------------------

    def run_all(self) -> list[CheckResult]:
        return [
            # formatter-guaranteed
            self.check_indentation(),
            self.check_heredoc_syntax(),
            self.check_double_quotes(),
            self.check_operator_spacing(),
            # content
            self.check_task_naming(),
            self.check_workflow_naming(),
            self.check_struct_naming(),
            self.check_call_aliases(),
            self.check_line_length(),
            self.check_set_pipefail(),
            self.check_parameter_meta(),
            self.check_docker_runtime(),
        ]


# ── display ───────────────────────────────────────────────────────────────────

_GUARANTEED = {
    "4-space indentation",
    "Heredoc (<<<) command syntax",
    "Double-quote string literals",
    "Spaces around = operator",
}

_ICON = {Status.PASS: "✓", Status.FAIL: "✗", Status.WARN: "!"}


def print_checklist(results: list[CheckResult], file=None) -> None:
    if file is None:
        file = sys.stderr

    guaranteed = [r for r in results if r.rule in _GUARANTEED]
    content = [r for r in results if r.rule not in _GUARANTEED]

    n_pass = sum(1 for r in results if r.status == Status.PASS)
    n_fail = sum(1 for r in results if r.status == Status.FAIL)
    n_warn = sum(1 for r in results if r.status == Status.WARN)

    width = 54
    print("\nBioWDL Style Guide Compliance", file=file)
    print("─" * width, file=file)
    print("  Formatter guarantees", file=file)
    for r in guaranteed:
        print(f"    {_ICON[r.status]}  {r.rule}", file=file)

    print("  Content checks", file=file)
    for r in content:
        line = f"    {_ICON[r.status]}  {r.rule}"
        if r.details and r.status != Status.PASS:
            line += f"\n         {r.details}"
        print(line, file=file)

    print("─" * width, file=file)
    parts = []
    if n_fail:
        parts.append(f"{n_fail} failed")
    if n_warn:
        parts.append(f"{n_warn} warning(s)")
    parts.append(f"{n_pass} passed")
    print(f"  {('  ·  ').join(parts)}", file=file)
    print(file=file)
