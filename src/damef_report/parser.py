from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class DamefRecord:
    company: str
    document_id: str
    state_registration: str
    base_year: int
    municipality: str
    state: str
    taxpayer_type: str
    economic_activity: str
    total_inputs: Decimal
    domestic_sales: Decimal
    interstate_sales: Decimal
    export_sales: Decimal
    total_outputs: Decimal
    value_added: Decimal
    source_file: str


def _match(pattern: str, text: str, default: str = "") -> str:
    found = re.search(pattern, text, re.MULTILINE)
    return " ".join(found.group(1).split()) if found else default


def parse_amount(raw: str) -> Decimal:
    value = raw.strip().replace(".", "").replace(",", ".")
    return Decimal(value) if value else Decimal("0")


def parse_damef_text(text: str, source_file: str = "") -> DamefRecord:
    sales_section = re.search(
        r"DAMEF - SAÍDAS \(VALOR CONTÁBIL\)(.*?)(?:VAF - EXCLUSÕES VAF)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    sales_text = sales_section.group(1) if sales_section else ""
    sales = re.search(r"VENDAS\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)", sales_text, re.IGNORECASE)
    return DamefRecord(
        company=_match(r"Contribuinte:\s*(.+)", text),
        document_id=_match(r"CNPJ:\s*([\d./-]+)", text),
        state_registration=_match(r"Inscrição Estadual\s*:\s*([\d.-]+)", text),
        base_year=int(_match(r"Ano Base:\s*(\d{4})", text, "0")),
        municipality=_match(r"Município:\s*(.+?)\s+UF:", text),
        state=_match(r"UF:\s*([A-Z]{2})", text),
        taxpayer_type=_match(r"Tipo:\s*(.+)", text),
        economic_activity=_match(r"CNAE:\s*([0-9/-]+)", text),
        total_inputs=parse_amount(_match(r"TOTAL DAS ENTRADAS\s*([\d.,]+)", text, "0")),
        domestic_sales=parse_amount(sales.group(1) if sales else "0"),
        interstate_sales=parse_amount(sales.group(2) if sales else "0"),
        export_sales=parse_amount(sales.group(3) if sales else "0"),
        total_outputs=parse_amount(_match(r"TOTAL DAS SAÍDAS\s*([\d.,]+)", text, "0")),
        value_added=parse_amount(_match(r"VAF\s*([\d.,]+)", text, "0")),
        source_file=source_file,
    )


def extract_damef_pdf(path: Path) -> DamefRecord:
    """Extract and parse a text-layer DAMEF PDF."""
    import pdfplumber

    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return parse_damef_text(text, path.name)
