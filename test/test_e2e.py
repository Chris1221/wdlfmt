import wdlformat
import wdlformat.utils
import pytest
import glob


@pytest.fixture
def collect_all_wdl_paths():
    biowdl_tasks = glob.glob("test/biowdl_tasks/*.wdl")
    examples = glob.glob("test/examples/*.wdl")

    return biowdl_tasks + examples


def test_all_examples(collect_all_wdl_paths):
    # Calling format_wdl is equivalent to asserting
    # that the formatting was successful.
    #
    # This because asserting that the content
    # does not change between the original
    # and formatted text.

    # We can actually just run all of these
    # at once but it's better to do it
    # one at a time to report errors
    assert len(collect_all_wdl_paths) > 1
    for wdl in collect_all_wdl_paths:
        print("WDL is now:", wdl)
        formatted = wdlformat.format_wdl(wdl, return_object=True)
        assert formatted
