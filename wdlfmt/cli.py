import argparse
import sys
from .visitor import format_wdl
from .checker import StyleChecker, print_checklist


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
    parser.add_argument(
        "--no-check",
        action="store_true",
        help="Skip the BioWDL style guide compliance checklist",
    )

    args = parser.parse_args()

    if not args.files:
        parser.print_help()
        return

    if args.in_place:
        format_wdl(files=args.files, in_place=True)
        return

    # Capture formatted text so we can both print it and run the checker.
    formatted_texts = format_wdl(files=args.files, in_place=False, return_object=True)
    if isinstance(formatted_texts, str):
        formatted_texts = [formatted_texts]

    for text in formatted_texts:
        sys.stdout.write(text)
        if not args.no_check:
            results = StyleChecker(text).run_all()
            print_checklist(results, file=sys.stderr)
