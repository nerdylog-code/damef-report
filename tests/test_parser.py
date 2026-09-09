from decimal import Decimal
from pathlib import Path

from damef_report.parser import parse_damef_text


TEXT = """Contribuinte: EMPRESA SINTETICA LTDA
CNPJ: 00.000.000/0000-00
Inscrição Estadual: 000.000.000.000
Ano Base: 2025
Município: CIDADE EXEMPLO UF: MG
Tipo: REGIME NORMAL
CNAE: 0000-0/00
TOTAL DAS ENTRADAS 1.234.567,89
DAMEF - SAÍDAS (VALOR CONTÁBIL)
VENDAS 100.000,00 20.000,00 5.000,00
TOTAL DAS SAÍDAS 125.000,00
VAF - EXCLUSÕES VAF
VAF 42.500,00
"""


def test_parse_synthetic_report() -> None:
    result = parse_damef_text(TEXT, "sample.txt")
    assert result.company == "EMPRESA SINTETICA LTDA"
    assert result.base_year == 2025
    assert result.domestic_sales == Decimal("100000.00")
    assert result.total_inputs == Decimal("1234567.89")
    assert result.value_added == Decimal("42500.00")


def test_missing_sales_section_is_safe() -> None:
    result = parse_damef_text("Contribuinte: TESTE\nAno Base: 2024")
    assert result.base_year == 2024
    assert result.domestic_sales == Decimal("0")
    assert result.total_outputs == Decimal("0")
