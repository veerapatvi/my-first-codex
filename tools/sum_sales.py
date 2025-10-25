#!/usr/bin/env python3
"""Aggregate sales totals from CSV files under a data directory."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable, Iterator, Tuple

DEFAULT_DATA_DIR = Path("data")
CURRENCY_PLACES = Decimal("0.01")


class NoMatchingFilesError(FileNotFoundError):
    """Raised when no CSV files match the provided pattern."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sum the values from the 'amount' column across every CSV file "
            "within a data directory."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--pattern",
        default="*.csv",
        help="Glob pattern used to select CSV files within the data directory.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Path to the directory containing CSV files to total.",
    )
    return parser.parse_args()


def iter_csv_files(data_dir: Path, pattern: str) -> Iterator[Path]:
    data_dir = data_dir.expanduser()
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory '{data_dir}' was not found.")
    if not data_dir.is_dir():
        raise NotADirectoryError(f"'{data_dir}' is not a directory.")

    for path in sorted(data_dir.rglob(pattern)):
        if path.is_file():
            yield path


def parse_amount(raw_amount: str, csv_path: Path, line_number: int) -> Decimal:
    sanitized = raw_amount.strip().replace(",", "")
    if not sanitized:
        raise ValueError(
            f"Missing amount value in '{csv_path}' on line {line_number}."
        )
    try:
        return Decimal(sanitized)
    except InvalidOperation as exc:
        raise ValueError(
            "Could not convert amount value "
            f"'{raw_amount}' to a number in '{csv_path}' (line {line_number})."
        ) from exc


def read_amounts(csv_path: Path) -> Iterable[Decimal]:
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames or "amount" not in reader.fieldnames:
            raise ValueError(
                f"CSV file '{csv_path}' must contain an 'amount' column."
            )
        for line_number, row in enumerate(reader, start=2):
            raw_amount = row.get("amount", "") or ""
            yield parse_amount(raw_amount, csv_path, line_number)


def calculate_total(data_dir: Path, pattern: str) -> Tuple[Decimal, int]:
    csv_files = list(iter_csv_files(data_dir, pattern))
    if not csv_files:
        raise NoMatchingFilesError(
            f"No files matching pattern '{pattern}' were found in '{data_dir}'."
        )

    total = Decimal("0")
    for csv_path in csv_files:
        total += sum(read_amounts(csv_path), Decimal("0"))

    return total, len(csv_files)


def format_currency(amount: Decimal) -> str:
    quantized = amount.quantize(CURRENCY_PLACES)
    return f"{quantized:,.2f}"


def main() -> None:
    args = parse_args()
    try:
        total, _ = calculate_total(args.data_dir, args.pattern)
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        raise SystemExit(str(exc))

    print(f"Total sales: {format_currency(total)}")


if __name__ == "__main__":
    main()
