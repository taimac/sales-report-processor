from __future__ import annotations

from pathlib import Path
import re
from typing import Any, List, Dict



TIMESTAMP_PATTERN = re.compile(
    r"(?P<date>\d{2}/\d{2}/\d{4})\s*-\s*(?P<time>\d{2}:\d{2}:\d{2})"
)

MAIN_ROW_PATTERN = re.compile(r"^\s*\d+\s+\d+\s+\d+\s+")

CONTINUATION_PATTERN = re.compile(r"^\s{10,}\d[\d\.\sA-Z]*")

MAIN_ROW_LEADING_PATTERN = re.compile(
    r"^\s*(?P<est>\d+)\s+(?P<pedido>\d+)\s+(?P<seq>\d+)\s+"
)

THICKNESS_PATTERN = re.compile(r"\d+,\d{2}")



def read_txt_report(file_path: str | Path) -> dict[str, Any]:
    """
    Read a TXT report safely, normalize line endings, preserve raw text,
    and extract generated date/time metadata.
    """
    path = Path(file_path)
    raw_bytes = path.read_bytes()

    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw_text = raw_bytes.decode("latin-1")

    normalized_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.replace("\x0c", "").rstrip() for line in normalized_text.split("\n")]

    metadata = extract_generated_datetime(lines)

    return {
        "raw_text": raw_text,
        "lines": lines,
        "metadata": metadata,
    }


def extract_generated_datetime(lines: list[str]) -> dict[str, str | None]:
    """
    Extract report generated date and time from the header area.
    Returns None values if not found.
    """
    for line in lines:
        match = TIMESTAMP_PATTERN.search(line)
        if match:
            return {
                "generated_date": match.group("date"),
                "generated_time": match.group("time"),
            }

    return {
        "generated_date": None,
        "generated_time": None,
    }

def is_blank(line: str) -> bool:
    return line.strip() == ""


def is_separator_line(line: str) -> bool:
    stripped = line.strip()
    return (
        len(stripped) > 10
        and (set(stripped) <= {"-", "="} or stripped.startswith("---"))
    )


def is_customer_header_line(line: str) -> bool:
    return "Rep:" in line and "Cliente:" in line


def is_table_header_line(line: str) -> bool:
    return "Est Pedido" in line and "Descrição" in line


def is_client_total_line(line: str) -> bool:
    return "TOT CLIENTE:" in line


def is_client_currency_total_line(line: str) -> bool:
    return "TOTAL CLIENTE EM R$:" in line


def is_grand_total_line(line: str) -> bool:
    return "TOTAL GERAL:" in line


def is_grand_currency_total_line(line: str) -> bool:
    return "TOTAL EM R$:" in line


def is_main_detail_row(line: str) -> bool:
    return bool(MAIN_ROW_PATTERN.match(line))


def is_continuation_row(line: str) -> bool:
    # continuation rows are indented and contain order references/status
    return (
        not is_main_detail_row(line)
        and bool(CONTINUATION_PATTERN.match(line))
    )


def classify_line(line: str) -> str:
    if is_blank(line):
        return "blank"
    if is_separator_line(line):
        return "separator"
    if is_customer_header_line(line):
        return "customer_header"
    if is_table_header_line(line):
        return "table_header"
    if is_client_total_line(line):
        return "client_total"
    if is_client_currency_total_line(line):
        return "client_total_currency"
    if is_grand_total_line(line):
        return "grand_total"
    if is_grand_currency_total_line(line):
        return "grand_total_currency"
    if is_main_detail_row(line):
        return "main_detail"
    if is_continuation_row(line):
        return "continuation"

    return "ignorable"


def classify_report_lines(lines: List[str]) -> List[Dict[str, str]]:
    return [{"line": line, "type": classify_line(line)} for line in lines]


def parse_customer_header(line: str) -> Dict[str, str]:
    # Example: "Rep: MACIEL       Cliente: FLANTECH"
    rep_match = re.search(r"Rep:\s*(\S+)", line)
    client_match = re.search(r"Cliente:\s*(.+)", line)

    return {
        "representative": rep_match.group(1) if rep_match else "",
        "customer_name": client_match.group(1).strip() if client_match else "",
    }


def detect_customer_blocks(lines: List[str]) -> List[Dict[str, Any]]:
    blocks = []
    current_block = None

    for line in lines:
        line_type = classify_line(line)

        if line_type == "customer_header":
            if current_block:
                blocks.append(current_block)

            header_data = parse_customer_header(line)

            current_block = {
                "header_line": line,
                "representative": header_data["representative"],
                "customer_name": header_data["customer_name"],
                "lines": [],
            }
            continue

        if current_block:
            current_block["lines"].append(
                {"line": line, "type": line_type}
            )

    if current_block:
        blocks.append(current_block)

    return blocks

def parse_main_row_identity_fields(line: str) -> dict[str, str]:
    """
    Parse the SRP-23 identity/product columns from a fixed-width main detail row.

    Fields:
    - est
    - pedido
    - seq
    - descricao
    - espess
    - larg
    - compr
    """
    if classify_line(line) != "main_detail":
        return {
            "raw_line": line,
            "est": "",
            "pedido": "",
            "seq": "",
            "descricao": "",
            "espess": "",
            "larg": "",
            "compr": "",
        }

    return {
        "raw_line": line,
        "est": line[0:2].strip(),
        "pedido": line[4:10].strip(),
        "seq": line[15:17].strip(),
        "descricao": line[18:56].strip(),
        "espess": line[59:63].strip(),
        "larg": line[64:72].strip(),
        "compr": line[84:88].strip(),
    }


def parse_main_detail_lines(lines: list[str]) -> list[dict[str, str]]:
    """
    Parse all lines classified as main_detail and return only SRP-23 fields.
    """
    parsed_rows: list[dict[str, str]] = []

    for line in lines:
        if classify_line(line) == "main_detail":
            parsed_rows.append(parse_main_row_identity_fields(line))

    return parsed_rows

def parse_main_row_operational_fields(line: str) -> dict[str, str]:
    """
    Parse SRP-18 operational and quantity columns from a main detail row.

    Strategy:
    - SRP-23 already parsed up to `compr`
    - from the remainder, use whitespace tokenization because numeric widths vary
    """
    if classify_line(line) != "main_detail":
        return {}

    remainder = line[88:].strip()
    parts = remainder.split()

    # Expected order in the remainder:
    # ord_prod, sit_ordem(optional like LC10), dt_entr, aa,
    # qt_ped, qt_pc, qt_prod, qt_fatur, sdo_estoq, sit...
    #
    # In some rows, sit_ordem is blank.
    # We detect date first, then infer what comes before it.

    date_index = next(
        (i for i, part in enumerate(parts) if re.fullmatch(r"\d{2}/\d{2}/\d{2}", part)),
        None,
    )

    if date_index is None or date_index < 1:
        return {
            "ord_prod": "",
            "sit_ordem": "",
            "dt_entr": "",
            "aa": "",
            "qt_ped": "",
            "qt_pc": "",
            "qt_prod": "",
            "qt_fatur": "",
            "sdo_estoq": "",
            "sit": "",
        }

    ord_prod = parts[0]
    sit_ordem = " ".join(parts[1:date_index]) if date_index > 1 else ""
    dt_entr = parts[date_index]
    aa = parts[date_index + 1] if len(parts) > date_index + 1 else ""
    qt_ped = parts[date_index + 2] if len(parts) > date_index + 2 else ""
    qt_pc = parts[date_index + 3] if len(parts) > date_index + 3 else ""
    qt_prod = parts[date_index + 4] if len(parts) > date_index + 4 else ""
    qt_fatur = parts[date_index + 5] if len(parts) > date_index + 5 else ""
    sdo_estoq = parts[date_index + 6] if len(parts) > date_index + 6 else ""
    sit = " ".join(parts[date_index + 7:]) if len(parts) > date_index + 7 else ""

    return {
        "ord_prod": ord_prod,
        "sit_ordem": sit_ordem,
        "dt_entr": dt_entr,
        "aa": aa,
        "qt_ped": qt_ped,
        "qt_pc": qt_pc,
        "qt_prod": qt_prod,
        "qt_fatur": qt_fatur,
        "sdo_estoq": sdo_estoq,
        "sit": sit,
    }

def parse_main_row_full_step_1(line: str) -> dict[str, str]:
    """
    Combine SRP-23 and SRP-18 parsing (identity + operational).
    """

    base = parse_main_row_identity_fields(line)
    operational = parse_main_row_operational_fields(line)

    return {
        **base,
        **operational,
    }

def parse_main_detail_lines_step_1(lines: list[str]) -> list[dict[str, str]]:
    results = []

    for line in lines:
        if classify_line(line) == "main_detail":
            results.append(parse_main_row_full_step_1(line))

    return results

def parse_main_row_commercial_fields(line: str) -> dict[str, str]:
    """
    Parse SRP-19 commercial and reference fields from the row tail.

    Strategy:
    - work from the remainder after `compr`
    - anchor on the date token
    - find the first price token (`pre_liq`)
    - support rows where `pf` is blank
    """
    empty_result = {
        "pre_liq": "",
        "pf": "",
        "vlr_peca": "",
        "pag": "",
        "transp": "",
        "cr_pro": "",
        "cr_fat": "",
        "o_compra": "",
        "item_cli": "",
        "mnf": "",
    }

    if classify_line(line) != "main_detail":
        return empty_result

    remainder = line[88:].strip()
    parts = remainder.split()

    date_index = next(
        (i for i, part in enumerate(parts) if re.fullmatch(r"\d{2}/\d{2}/\d{2}", part)),
        None,
    )
    if date_index is None:
        return empty_result

    # After date:
    # aa, qt_ped, qt_pc, qt_prod, qt_fatur, sdo_estoq, sit..., pre_liq, ...
    tail_start = date_index + 7

    price_index = next(
        (
            i
            for i in range(tail_start, len(parts))
            if re.fullmatch(r"\d+,\d{3}", parts[i])
        ),
        None,
    )
    if price_index is None:
        return empty_result

    commercial_parts = parts[price_index:]

    pre_liq = commercial_parts[0] if len(commercial_parts) > 0 else ""

    pf = ""
    vlr_peca = ""
    pag = ""
    transp = ""
    cr_pro = ""
    cr_fat = ""
    o_compra = ""
    item_cli = ""
    mnf = ""

    # Case 1: only one monetary token appears after pre_liq
    # Map it to PF and leave vlr_peca blank
    if (
        len(commercial_parts) >= 3
        and re.fullmatch(r"\d+,\d{3}", commercial_parts[1])
        and commercial_parts[2].isdigit()
    ):
        pf = commercial_parts[1]
        vlr_peca = ""
        pag = commercial_parts[2]
        transp = commercial_parts[3] if len(commercial_parts) > 3 else ""
        cr_pro = commercial_parts[4] if len(commercial_parts) > 4 else ""
        cr_fat = commercial_parts[5] if len(commercial_parts) > 5 else ""
        o_compra = commercial_parts[6] if len(commercial_parts) > 6 else ""
        item_cli = commercial_parts[7] if len(commercial_parts) > 7 else ""
        mnf = commercial_parts[8] if len(commercial_parts) > 8 else ""
    else:
        # Case 2: PF is present
        pf = commercial_parts[1] if len(commercial_parts) > 1 else ""
        vlr_peca = commercial_parts[2] if len(commercial_parts) > 2 else ""
        pag = commercial_parts[3] if len(commercial_parts) > 3 else ""
        transp = commercial_parts[4] if len(commercial_parts) > 4 else ""
        cr_pro = commercial_parts[5] if len(commercial_parts) > 5 else ""
        cr_fat = commercial_parts[6] if len(commercial_parts) > 6 else ""
        o_compra = commercial_parts[7] if len(commercial_parts) > 7 else ""
        item_cli = commercial_parts[8] if len(commercial_parts) > 8 else ""
        mnf = commercial_parts[9] if len(commercial_parts) > 9 else ""

    return {
        "pre_liq": pre_liq,
        "pf": pf,
        "vlr_peca": vlr_peca,
        "pag": pag,
        "transp": transp,
        "cr_pro": cr_pro,
        "cr_fat": cr_fat,
        "o_compra": o_compra,
        "item_cli": item_cli,
        "mnf": mnf,
    }

def parse_main_row_full(line: str) -> dict[str, str]:
    return {
        **parse_main_row_identity_fields(line),
        **parse_main_row_operational_fields(line),
        **parse_main_row_commercial_fields(line),
    }

def parse_main_detail_lines_full(lines: list[str]) -> list[dict[str, str]]:
    results = []

    for line in lines:
        if classify_line(line) == "main_detail":
            results.append(parse_main_row_full(line))

    return results

def parse_continuation_row(line: str) -> dict[str, str]:
    parts = line.strip().split()

    empty = {
        "raw_line": line,
        "ord_prod": "",
        "sit_ordem": "",
        "qt_prod": "",
        "sit": "",
    }

    if not parts:
        return empty

    ord_prod = parts[0]

    # Status is usually the trailing text after the last numeric quantity token
    last_numeric_index = None
    for i in range(len(parts) - 1, 0, -1):
        token = parts[i]
        if any(ch.isdigit() for ch in token):
            last_numeric_index = i
            break

    if last_numeric_index is None:
        return {
            **empty,
            "ord_prod": ord_prod,
            "sit": " ".join(parts[1:]).strip(),
        }

    qt_prod = parts[last_numeric_index]
    sit = " ".join(parts[last_numeric_index + 1:]).strip()
    sit_ordem = " ".join(parts[1:last_numeric_index - 1]).strip() if last_numeric_index > 2 else ""

    return {
        "raw_line": line,
        "ord_prod": ord_prod,
        "sit_ordem": sit_ordem,
        "qt_prod": qt_prod,
        "sit": sit,
    }

def attach_continuation_rows(lines: list[str]) -> list[dict]:
    """
    Attach continuation rows to their corresponding main rows.
    """
    results: list[dict] = []
    current_parent: dict | None = None

    for line in lines:
        line_type = classify_line(line)

        if line_type == "main_detail":
            current_parent = parse_main_row_full(line)
            current_parent["continuations"] = []
            results.append(current_parent)

        elif line_type == "continuation" and current_parent is not None:
            current_parent["continuations"].append(parse_continuation_row(line))

    return results

def extract_numeric_values(line: str) -> list[str]:
    """
    Extract numeric values like:
    1.234,56 or 123 or 12.000
    """
    return re.findall(r"\d[\d\.\,]*", line)


def parse_client_total_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_ped": values[0] if len(values) > 0 else "",
        "total_pc": values[1] if len(values) > 1 else "",
        "total_prod": values[2] if len(values) > 2 else "",
        "total_fatur": values[3] if len(values) > 3 else "",
        "total_sdo": values[4] if len(values) > 4 else "",
    }

def parse_client_total_currency_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_valor": values[0] if values else "",
    }

def parse_grand_total_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_ped": values[0] if len(values) > 0 else "",
        "total_pc": values[1] if len(values) > 1 else "",
        "total_prod": values[2] if len(values) > 2 else "",
        "total_fatur": values[3] if len(values) > 3 else "",
        "total_sdo": values[4] if len(values) > 4 else "",
    }

def parse_grand_total_currency_line(line: str) -> dict[str, str]:
    values = extract_numeric_values(line)

    return {
        "total_valor": values[0] if values else "",
    }

def extract_totals(lines: list[str]) -> dict[str, list[dict]]:
    """
    Extract all totals from the report.
    """

    results = {
        "client_totals": [],
        "client_total_currency": [],
        "grand_totals": [],
        "grand_total_currency": [],
    }

    for line in lines:
        line_type = classify_line(line)

        if line_type == "client_total":
            results["client_totals"].append(parse_client_total_line(line))

        elif line_type == "client_total_currency":
            results["client_total_currency"].append(
                parse_client_total_currency_line(line)
            )

        elif line_type == "grand_total":
            results["grand_totals"].append(parse_grand_total_line(line))

        elif line_type == "grand_total_currency":
            results["grand_total_currency"].append(
                parse_grand_total_currency_line(line)
            )

    return results