# CSV report automation (portfolio example)

This is a small, synthetic portfolio example of a repeatable CSV cleaning and reporting job. It is explicitly a demonstration artifact, not a client deliverable or a promise of production readiness. It uses only Python's standard library and does not require a database.

The command validates `transaction_id`, ISO date, category, and decimal amount; skips invalid rows; counts each transaction ID once; sorts output deterministically; and writes `cleaned.csv` plus `summary.json`.

## Quickstart

From this directory:

```text
python csv_report.py sample_transactions.csv demo-output
python -m unittest -v
```

Observed output for the included sample:

```json
{
  "rows_read": 6,
  "rows_written": 3,
  "invalid_rows": 2,
  "duplicate_rows": 1,
  "total_amount": "35.59",
  "totals_by_category": {
    "office": "15.60",
    "software": "19.99"
  }
}
```

The CLI also reports the input filename and exact validation messages. Re-running with the same input replaces the two generated files with byte-for-byte identical content.
