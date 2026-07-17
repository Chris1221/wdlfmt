"""Regenerate all snapshot .expected.wdl files from their .input.wdl counterparts.

Run from the repo root:
    python scripts/update_snapshots.py

Review the diffs before committing — these files define the formatter's expected output.
"""

from pathlib import Path

import wdlfmt

SNAPSHOT_DIR = Path(__file__).parent.parent / "test" / "snapshots"


def main():
    inputs = sorted(SNAPSHOT_DIR.glob("*.input.wdl"))
    if not inputs:
        print(f"No *.input.wdl files found in {SNAPSHOT_DIR}")
        return

    for input_path in inputs:
        expected_path = input_path.with_name(
            input_path.name.replace(".input.wdl", ".expected.wdl")
        )
        result = wdlfmt.format_wdl_str(input_path.read_text())
        expected_path.write_text(result)
        print(f"Updated {expected_path.name}")


if __name__ == "__main__":
    main()
