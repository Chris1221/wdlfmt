import argparse
from .visitor import format_wdl


def cli():
    parser = argparse.ArgumentParser(description="Black, for WDL.")
    parser.add_argument(
        "files",
        metavar="file",
        nargs="*",
        help="WDL files to format",
    )
    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Edit files in place",
    )

    format_wdl(**vars(parser.parse_args()))
