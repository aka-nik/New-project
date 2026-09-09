"""Print basic profiling information for CSV source tables."""

import argparse
import csv
from pathlib import Path


def profile_csv(path: Path) -> tuple[int, list[str]]:
    """Return the row count and column names for one CSV file."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        columns = next(reader)
        row_count = sum(1 for _ in reader)
    return row_count, columns


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source_dir",
        type=Path,
        help="Directory containing CSV source files",
    )
    arguments = parser.parse_args()

    paths = sorted(arguments.source_dir.glob("*.csv"))
    if not paths:
        raise SystemExit(f"No CSV files found in {arguments.source_dir}")

    for path in paths:
        row_count, columns = profile_csv(path)
        print(f"{path.name}: {row_count:,} rows, {len(columns)} columns")
        print(f"  columns: {', '.join(columns)}")


if __name__ == "__main__":
    main()
