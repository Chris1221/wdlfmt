# Testing the shell formatter
import pytest
import wdlfmt.formatters.shell_formatter as sf
import wdlfmt.utils as utils


@pytest.fixture
def input():
    return """
    set -e -o pipefail
    mkdir -p "$(dirname ~{combinedFilePath})"
    ~{cmdPrefix} ~{sep=" " fileList} ~{cmdSuffix} > ~{combinedFilePath}
    """


def test_shfmt_substitution(input):
    formatter = sf.ShfmtFormatter(input)
    output = formatter.format()

    utils.assert_text_equal(output, input)
