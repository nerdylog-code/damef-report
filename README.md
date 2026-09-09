# DAMEF Report

A local-first Python application that parses text-layer DAMEF fiscal reports and produces a consolidated Excel workbook for review. It demonstrates structured extraction, decimal-safe amount parsing, grouping by company/year, and deterministic reporting.

This is a sanitized portfolio repository. The included report is synthetic and intentionally uses invalid placeholder identifiers. No real PDF, taxpayer data, customer workbook, or operational output is included.

## Features

- Extract taxpayer label, identifier, state registration, year, location, activity, sales and value-added fields.
- Parse Brazilian thousands/decimal notation with `Decimal` before writing numeric workbook values.
- Build `Consolidado` and `Resumo` sheets.
- Batch-process local text-layer PDFs.
- Run a deterministic demo without credentials or external APIs.

## Quickstart

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python demo.py
```

The demo reads `fixtures/synthetic_damef.txt` and creates `output/demo_damef.xlsx`.

For real text-layer PDFs:

```bash
python -m damef_report.cli ./path/to/pdf-directory --output output/damef_report.xlsx
```

## Development

```bash
python -m pip install -e ".[test]"
python -m pytest
```

## Scope and limitations

- PDF extraction uses `pdfplumber` and expects a text layer; scanned-image OCR is outside this repository.
- DAMEF layouts can vary by issuing system. Add and test a fixture before relying on a new layout.
- The tool creates a review workbook; it does not file taxes, connect to government systems, or make accounting judgments.
- Keep real inputs and outputs outside version control and follow applicable privacy rules.
- No production, scale, savings, deployment, or coverage claims are made.

## License

MIT. See `LICENSE`.
