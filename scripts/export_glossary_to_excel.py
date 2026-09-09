from pathlib import Path
import csv

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font
except ModuleNotFoundError as exc:
    raise SystemExit("openpyxl is required. Install it with: .\\.venv\\Scripts\\python.exe -m pip install openpyxl") from exc


def parse_glossary(path: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    current_section = ""

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        if line.startswith("- **") and ":**" in line:
            title, description = line[3:].split(":**", 1)
            keyword = title.strip()
            definition = description.strip().rstrip("*")
            rows.append((current_section, keyword, definition))

    return rows


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    glossary_path = root / "docs" / "glossary.md"
    rows = parse_glossary(glossary_path)

    wb = Workbook()
    ws = wb.active
    ws.title = "Keywords"
    ws.append(["Section", "Keyword", "Definition"])
    for section, keyword, definition in rows:
        ws.append([section, keyword, definition])

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for column_cells in ws.columns:
        max_len = max(
            len(str(cell.value)) if cell.value is not None else 0
            for cell in column_cells
        )
        ws.column_dimensions[column_cells[0].column_letter].width = min(max_len + 2, 60)

    ws.freeze_panes = "A2"

    xlsx_path = root / "docs" / "sentineletl_keywords.xlsx"
    csv_path = root / "docs" / "sentineletl_keywords.csv"

    wb.save(xlsx_path)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Section", "Keyword", "Definition"])
        writer.writerows(rows)

    print(f"Created Excel: {xlsx_path}")
    print(f"Created CSV: {csv_path}")
    print(f"Keywords exported: {len(rows)}")


if __name__ == "__main__":
    main()
