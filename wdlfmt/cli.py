import argparse
import sys
from .visitor import format_wdl, format_wdl_str
from .checker import StyleChecker, print_checklist


def cli():
    parser = argparse.ArgumentParser(description="Black, for WDL.")
    parser.add_argument(
        "files",
        metavar="file",
        nargs="*",
        help="WDL files to format",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Edit files in place",
    )
    mode.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="Exit 1 if any file would be reformatted; do not write output",
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

    if args.check:
        failures = []
        for path in args.files:
            content = open(path).read()
            if format_wdl_str(content) != content:
                sys.stderr.write(f"would reformat: {path}\n")
                failures.append(path)
        n = len(args.files)
        if failures:
            sys.stderr.write(
                f"{len(failures)} file(s) would be reformatted, "
                f"{n - len(failures)} file(s) already correctly formatted.\n"
            )
            sys.exit(1)
        sys.stderr.write(f"{n} file(s) already correctly formatted.\n")
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
