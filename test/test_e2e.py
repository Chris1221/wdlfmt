import glob
import subprocess

import pytest

import wdlfmt


def collect_all_wdl_paths():
    biowdl_tasks = glob.glob("test/biowdl_tasks/*.wdl")
    examples = glob.glob("test/examples/*.wdl")

    # return ["test/biowdl_tasks/common.wdl"]
    return biowdl_tasks[0:10]


@pytest.mark.parametrize("file", collect_all_wdl_paths())
def test_all_examples_cli(file):
    # Calling format_wdl is equivalent to asserting
    # that the formatting was successful.
    #
    # This because asserting that the content
    # does not change between the original
    # and formatted text.

    # We can actually just run all of these
    # at once but it's better to do it
    # one at a time to report errors
    # wdlfmt.format_wdl(file)
    assert subprocess.run(["wdlfmt", file], shell=True).returncode == 0


@pytest.mark.parametrize("file", collect_all_wdl_paths())
def test_all_examples_raw(file):
    wdlfmt.format_wdl(file)
