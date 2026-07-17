import unittest
from pathlib import Path

import wdlfmt

SNAPSHOT_DIR = Path(__file__).parent / "snapshots"

KNOWN_NON_IDEMPOTENT: set = set()


def snapshot_pairs():
    return [
        (p, p.with_name(p.name.replace(".input.wdl", ".expected.wdl")))
        for p in sorted(SNAPSHOT_DIR.glob("*.input.wdl"))
    ]


def _make_test(input_path, expected_path):
    def test(self):
        result = wdlfmt.format_wdl_str(input_path.read_text())
        self.assertEqual(result, expected_path.read_text())

    return test


def _make_idempotency_test(expected_path):
    def test(self):
        expected = expected_path.read_text()
        self.assertEqual(wdlfmt.format_wdl_str(expected), expected)

    return test


class TestSnapshots(unittest.TestCase):
    pass


for _inp, _exp in snapshot_pairs():
    _name = _inp.stem.replace(".input", "")

    setattr(TestSnapshots, f"test_{_name}", _make_test(_inp, _exp))

    idempotency_test = _make_idempotency_test(_exp)
    if _name in KNOWN_NON_IDEMPOTENT:
        idempotency_test = unittest.expectedFailure(idempotency_test)
    setattr(TestSnapshots, f"test_{_name}_idempotent", idempotency_test)


if __name__ == "__main__":
    unittest.main()
