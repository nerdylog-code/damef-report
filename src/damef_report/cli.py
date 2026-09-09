from __future__ import annotations

import argparse
from pathlib import Path

from .parser import extract_damef_pdf
from .workbook import build_workbook


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a workbook from DAMEF PDFs")
    parser.add_argument("input_dir", type=Path, help="directory containing PDF reports")
    parser.add_argument("-o", "--output", type=Path, default=Path("output/damef_report.xlsx"))
    args = parser.parse_args()
    paths = sorted(args.input_dir.glob("*.pdf"))
    if not paths:
        parser.error(f"no PDF files found in {args.input_dir}")
    records = [extract_damef_pdf(path) for path in paths]
    build_workbook(records, args.output)
    print(f"processed={len(records)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
