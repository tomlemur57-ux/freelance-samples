"""Portfolio example: validate a small CSV and produce a deterministic report."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED_COLUMNS = ("transaction_id", "date", "category", "amount")


@dataclass(frozen=True)
class CleanRow:
    transaction_id: str
    date: str
    category: str
    amount: Decimal


def parse_amount(raw: str) -> Decimal:
    """Parse a money value without introducing binary floating-point rounding."""
    value = Decimal(raw.strip())
    if not value.is_finite():
        raise InvalidOperation
    return value.quantize(Decimal("0.01"))


def validate_row(row: dict[str, str], line_number: int) -> CleanRow:
    missing = [column for column in REQUIRED_COLUMNS if not (row.get(column) or "").strip()]
    if missing:
        raise ValueError(f"line {line_number}: missing {', '.join(missing)}")

    try:
        date.fromisoformat(row["date"].strip())
    except ValueError as exc:
        raise ValueError(f"line {line_number}: date must be YYYY-MM-DD") from exc

    try:
        amount = parse_amount(row["amount"])
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"line {line_number}: amount must be a valid number") from exc

    return CleanRow(
        transaction_id=row["transaction_id"].strip(),
        date=row["date"].strip(),
        category=row["category"].strip(),
        amount=amount,
    )


def process_csv(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Process *input_path*, writing cleaned.csv and summary.json to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[CleanRow] = []
    errors: list[str] = []
    duplicate_count = 0
    seen_ids: set[str] = set()

    with input_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        missing_columns = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing_columns:
            raise ValueError(f"input is missing required columns: {', '.join(missing_columns)}")
        for line_number, row in enumerate(reader, start=2):
            try:
                clean_row = validate_row(row, line_number)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            if clean_row.transaction_id in seen_ids:
                duplicate_count += 1
                continue
            seen_ids.add(clean_row.transaction_id)
            rows.append(clean_row)

    rows.sort(key=lambda row: (row.date, row.category, row.transaction_id))
    with (output_dir / "cleaned.csv").open("w", newline="", encoding="utf-8") as cleaned:
        writer = csv.DictWriter(cleaned, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "transaction_id": row.transaction_id,
                "date": row.date,
                "category": row.category,
                "amount": f"{row.amount:.2f}",
            })

    totals: dict[str, Decimal] = {}
    for row in rows:
        totals[row.category] = totals.get(row.category, Decimal("0")) + row.amount
    summary = {
        "input_file": input_path.name,
        "rows_read": len(rows) + len(errors) + duplicate_count,
        "rows_written": len(rows),
        "invalid_rows": len(errors),
        "duplicate_rows": duplicate_count,
        "total_amount": f"{sum(totals.values(), Decimal('0')):.2f}",
        "totals_by_category": {category: f"{totals[category]:.2f}" for category in sorted(totals)},
        "errors": errors,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a CSV and write a clean report (portfolio example).")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    summary = process_csv(args.input_csv, args.output_dir)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
