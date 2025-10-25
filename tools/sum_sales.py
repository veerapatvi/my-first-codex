#!/usr/bin/env python3
"""Aggregate sales amounts from CSV files under the data directory."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

DATA_DIR = Path("data")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sum the values from the 'amount' column across every CSV file in the"
            " data directory."
        )
    )
    parser.add_argument(
        "--pattern",
        default="*.csv",
        help="Glob pattern used to select CSV files within the data directory.",
    )
    return parser.parse_args()


def read_amounts(csv_path: Path) -> Iterable[float]:
    with csv_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or "amount" not in reader.fieldnames:
            raise ValueError(
                f"CSV file '{csv_path}' must contain an 'amount' column."
            )
        for line_number, row in enumerate(reader, start=2):
            raw_amount = row.get("amount", "")
            if raw_amount in {None, ""}:
                raise ValueError(
                    f"Missing amount value in '{csv_path}' on line {line_number}."
                )
            try:
                yield float(raw_amount)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "Could not convert amount value "
                    f"'{raw_amount}' to a number in '{csv_path}' (line {line_number})."
                ) from exc


def iter_csv_files(pattern: str) -> Iterable[Path]:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory '{DATA_DIR}' was not found.")
    for path in sorted(DATA_DIR.rglob(pattern)):
        if path.is_file():
            yield path


def main() -> None:
    args = parse_args()
    total = 0.0
    files_processed = 0

    for csv_path in iter_csv_files(args.pattern):
        total += sum(read_amounts(csv_path))
        files_processed += 1

    if files_processed == 0:
        raise SystemExit(
            f"No files matching pattern '{args.pattern}' were found in '{DATA_DIR}'."
        )

    print(f"Total sales: {total:,.2f}")


if __name__ == "__main__":
    main()
