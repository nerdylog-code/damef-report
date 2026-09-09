from pathlib import Path

from damef_report.parser import parse_damef_text
from damef_report.workbook import build_workbook


ROOT = Path(__file__).parent
fixture = ROOT / "fixtures" / "synthetic_damef.txt"
record = parse_damef_text(fixture.read_text(encoding="utf-8"), fixture.name)
output = ROOT / "output" / "demo_damef.xlsx"
build_workbook([record], output)
print(f"company={record.company} year={record.base_year} output={output}")
