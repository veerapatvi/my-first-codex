#!/usr/bin/env python3
"""Summarize transaction amounts in a CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute the total amount from a CSV file with date and amount columns."
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Path to a CSV file containing 'date' and 'amount' columns.",
    )
    return parser.parse_args()


def read_amounts(csv_path: Path) -> Iterable[float]:
    with csv_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if "amount" not in reader.fieldnames:
            raise ValueError("CSV file must contain an 'amount' column.")
        for row in reader:
            try:
                yield float(row["amount"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Could not convert amount value '{row['amount']}' to a number."
                ) from exc


def main() -> None:
    args = parse_arguments()
    amounts = list(read_amounts(args.csv_path))
    total = sum(amounts)
    print(f"Total amount: {total:.2f}")


if __name__ == "__main__":
    main()
