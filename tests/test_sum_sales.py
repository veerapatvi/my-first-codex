import csv
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import sum_sales


def write_csv(path: Path, rows: list[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["date", "amount"])
        writer.writerows(rows)


def test_calculate_total_single_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "sales.csv"
    write_csv(csv_path, [("2024-01-01", "10.50"), ("2024-01-02", "20.25")])

    total, file_count = sum_sales.calculate_total(tmp_path, "*.csv")

    assert total == Decimal("30.75")
    assert file_count == 1


def test_calculate_total_handles_commas(tmp_path: Path) -> None:
    (tmp_path / "north").mkdir()
    write_csv(tmp_path / "north" / "region.csv", [("2024-02-01", "1,200.40")])
    write_csv(tmp_path / "summary.csv", [("2024-02-02", "50")])

    total, file_count = sum_sales.calculate_total(tmp_path, "*.csv")

    assert total == Decimal("1250.40")
    assert file_count == 2


def test_invalid_amount_raises_value_error(tmp_path: Path) -> None:
    csv_path = tmp_path / "bad.csv"
    write_csv(csv_path, [("2024-03-01", "not-a-number")])

    with pytest.raises(ValueError):
        sum_sales.calculate_total(tmp_path, "*.csv")


def test_missing_files_raises(tmp_path: Path) -> None:
    with pytest.raises(sum_sales.NoMatchingFilesError):
        sum_sales.calculate_total(tmp_path, "*.csv")
