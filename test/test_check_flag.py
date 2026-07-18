"""Tests for the --check / -c CLI flag and is_formatted() API."""
import subprocess
from pathlib import Path

import pytest

import wdlfmt

SNAPSHOT_DIR = Path(__file__).parent / "snapshots"


def expected_paths():
    return sorted(SNAPSHOT_DIR.glob("*.expected.wdl"))


def input_paths():
    return sorted(SNAPSHOT_DIR.glob("*.input.wdl"))


# ---------------------------------------------------------------------------
# Python API tests
# ---------------------------------------------------------------------------


def test_is_formatted_true_for_expected_snapshots():
    for path in expected_paths():
        content = path.read_text()
        assert wdlfmt.is_formatted(content), f"{path.name} should already be formatted"


def test_is_formatted_false_for_input_snapshots():
    for path in input_paths():
        content = path.read_text()
        assert not wdlfmt.is_formatted(content), f"{path.name} should need formatting"


def test_is_formatted_idempotent_on_already_formatted():
    raw = "version 1.0\ntask Foo {\n  input {\n  }\n}\n"
    formatted = wdlfmt.format_wdl_str(raw)
    assert wdlfmt.is_formatted(formatted)


def test_is_formatted_false_for_unindented_wdl():
    wdl = "version 1.0\ntask Foo {\ninput {\n}\n}\n"
    assert not wdlfmt.is_formatted(wdl)


# ---------------------------------------------------------------------------
# CLI --check flag tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", expected_paths())
def test_check_passes_on_formatted_files(path):
    result = subprocess.run(
        ["wdlfmt", "--check", str(path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Expected exit 0 for {path.name}, got {result.returncode}\n{result.stderr}"
    )


@pytest.mark.parametrize("path", input_paths())
def test_check_fails_on_unformatted_files(path):
    result = subprocess.run(
        ["wdlfmt", "--check", str(path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, (
        f"Expected exit 1 for {path.name}, got {result.returncode}"
    )


def test_check_short_flag_works():
    path = expected_paths()[0]
    result = subprocess.run(
        ["wdlfmt", "-c", str(path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_reports_which_files_would_be_reformatted():
    path = input_paths()[0]
    result = subprocess.run(
        ["wdlfmt", "--check", str(path)],
        capture_output=True,
        text=True,
    )
    assert "would reformat" in result.stderr
    assert str(path) in result.stderr


def test_check_exits_1_when_mix_of_formatted_and_unformatted():
    formatted = str(expected_paths()[0])
    unformatted = str(input_paths()[0])
    result = subprocess.run(
        ["wdlfmt", "--check", formatted, unformatted],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1


def test_check_and_in_place_are_mutually_exclusive():
    path = str(expected_paths()[0])
    result = subprocess.run(
        ["wdlfmt", "--check", "-i", path],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_does_not_write_to_stdout():
    path = str(input_paths()[0])
    result = subprocess.run(
        ["wdlfmt", "--check", path],
        capture_output=True,
        text=True,
    )
    assert result.stdout == ""
