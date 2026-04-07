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