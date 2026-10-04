import csv
import json
import tempfile
import unittest
from pathlib import Path

from csv_report import process_csv


class CsvReportTests(unittest.TestCase):
    def write_input(self, directory: Path, text: str) -> Path:
        path = directory / "input.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_invalid_rows_are_excluded_and_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_input(
                root,
                "transaction_id,date,category,amount\n"
                "ok,2026-01-01,office,0.10\n"
                "bad,wrong,office,1.00\n",
            )
            summary = process_csv(source, root / "out")
            self.assertEqual(summary["rows_written"], 1)
            self.assertEqual(summary["invalid_rows"], 1)
            self.assertEqual(summary["total_amount"], "0.10")
            self.assertIn("date must be YYYY-MM-DD", summary["errors"][0])

    def test_short_rows_are_reported_as_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_input(
                root,
                "transaction_id,date,category,amount\n"
                "short,2026-01-01,office\n",
            )
            summary = process_csv(source, root / "out")
            self.assertEqual(summary["rows_read"], 1)
            self.assertEqual(summary["rows_written"], 0)
            self.assertEqual(summary["invalid_rows"], 1)
            self.assertIn("missing amount", summary["errors"][0])

    def test_duplicate_ids_count_once_and_reruns_are_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = self.write_input(
                root,
                "transaction_id,date,category,amount\n"
                "b,2026-01-02,software,0.20\n"
                "a,2026-01-01,office,0.30\n"
                "b,2026-01-02,software,0.20\n",
            )
            first = process_csv(source, root / "out")
            clean_first = (root / "out" / "cleaned.csv").read_text(encoding="utf-8")
            summary_first = (root / "out" / "summary.json").read_text(encoding="utf-8")
            second = process_csv(source, root / "out")
            self.assertEqual(first, second)
            self.assertEqual(clean_first, (root / "out" / "cleaned.csv").read_text(encoding="utf-8"))
            self.assertEqual(summary_first, (root / "out" / "summary.json").read_text(encoding="utf-8"))
            with (root / "out" / "cleaned.csv").open(newline="", encoding="utf-8") as handle:
                self.assertEqual([row["transaction_id"] for row in csv.DictReader(handle)], ["a", "b"])
            self.assertEqual(json.loads(summary_first)["duplicate_rows"], 1)


if __name__ == "__main__":
    unittest.main()
